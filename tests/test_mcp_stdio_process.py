"""Independent MCP SDK client drives the real stdio server subprocess."""

import anyio
import base64
import json
import os
from io import BytesIO
from pathlib import Path
import sys

from jsonschema import validate
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from chatgpt_study_system.adapters.history import SQLiteHistoryBackend
from chatgpt_study_system.contracts import HistoryImportItem


def test_independent_stdio_client_uses_configured_gateway_and_resources(tmp_path: Path) -> None:
    study = tmp_path / "study"
    assets = tmp_path / "assets"
    source_root = tmp_path / "pdf-sources"
    study.mkdir()
    assets.mkdir()
    source_root.mkdir()
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    content = writer._add_object(DecodedStreamObject())
    content.set_data(b"BT /F1 12 Tf 10 80 Td (Independent MCP document) Tj ET")
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)}),
    })
    page[NameObject("/Contents")] = content
    pdf_out = BytesIO()
    writer.write(pdf_out)
    (source_root / "mcp-fixture.pdf").write_bytes(pdf_out.getvalue())
    history_db = tmp_path / "history.db"
    asset_db = tmp_path / "assets.db"
    history = SQLiteHistoryBackend(history_db)
    history.register_source("synthetic-export", "Synthetic export")
    history.import_items("synthetic-export", [HistoryImportItem(
        "entry-1", "conversation-1", "user", "Synthetic quadratic question",
        "2026-09-25T12:00:00Z",
    )])
    config = tmp_path / "runtime.toml"
    config.write_text(
        '[gateway]\nversion="0.1.0"\n[study]\n'
        f'root={json.dumps(study.as_posix())}\nqmd_collection="studyvault"\nqmd_version="2.8.3"\n'
        'qmd_executable="synthetic-qmd-not-installed"\n'
        '[history]\nbackend="sqlite"\n'
        f'database={json.dumps(history_db.as_posix())}\n'
        '[assets]\nbackend="sqlite"\n'
        f'root={json.dumps(assets.as_posix())}\n'
        f'database={json.dumps(asset_db.as_posix())}\n'
        f'ingest_root={json.dumps(source_root.as_posix())}\n'
        '[permissions]\ncapabilities=["read", "ingest"]\n',
        encoding="utf-8",
    )
    repository = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repository / "src") + os.pathsep + env.get("PYTHONPATH", "")
    params = StdioServerParameters(
        command=sys.executable,
        args=["-B", "-m", "chatgpt_study_system.transports.mcp_stdio", "--config", str(config)],
        env=env,
        cwd=repository,
    )

    async def check() -> None:
        with anyio.fail_after(20):
            async with stdio_client(params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as client:
                    await client.initialize()
                    tools = {tool.name: tool for tool in (await client.list_tools()).tools}
                    assert {"health_report", "search_study", "search_history", "fetch_history_item",
                            "ingest_documents", "ingest_document_file", "search_documents",
                            "fetch_document_page", "list_document_ocr_candidates",
                            "process_document_ocr_pages"} <= set(tools)
                    assert {"document_page", "document_page_image"} <= {
                        item.name for item in (await client.list_resource_templates()).resourceTemplates
                    }
                    workflow = next(item for item in (await client.list_resources()).resources
                                    if str(item.uri) == "study-workflow://wrong-answer")
                    workflow_body = (await client.read_resource(str(workflow.uri))).contents[0].text
                    prompt = next(item for item in (await client.list_prompts()).prompts
                                  if item.name == "wrong_answer_workflow")
                    prompt_body = (await client.get_prompt(prompt.name)).messages[0].content.text
                    assert prompt_body == workflow_body
                    assert "original visual" in workflow_body.lower()
                    assert "explicit request to save" in workflow_body.lower()
                    assert "save_wrong_answer_analysis" not in tools
                    validate({"query": "quadratic"}, tools["search_history"].inputSchema)

                    health = await client.call_tool("health_report", {})
                    assert health.structuredContent["ok"] is True
                    study_error = await client.call_tool("search_study", {"query": "synthetic"})
                    assert study_error.isError is True
                    assert study_error.structuredContent["error"]["code"] == "QMD_NOT_FOUND"
                    history_result = await client.call_tool("search_history", {"query": "quadratic"})
                    assert history_result.structuredContent["results"][0]["source_id"] == "synthetic-export"

                    document = await client.call_tool("ingest_documents", {"documents": [{
                        "title": "Synthetic chapter", "media_type": "text/plain",
                        "content_base64": base64.b64encode(b"MCP process fixture").decode("ascii"),
                    }]})
                    document_uri = document.structuredContent["documents"][0]["document_uri"]
                    found = await client.call_tool("search_documents", {"query": "fixture"})
                    assert found.structuredContent["total"] == 1
                    page = await client.read_resource(document_uri + "/page/1")
                    assert page.contents[0].text == "MCP process fixture"
                    assert page.contents[0].meta["text_origin"] == "source_text"
                    assert page.contents[0].meta["source_asset_uri"].startswith("asset://sha256/")

                    file_document = await client.call_tool("ingest_document_file", {
                        "relative_path": "mcp-fixture.pdf", "title": "Synthetic file source",
                    })
                    assert file_document.structuredContent["ok"] is True
                    file_uri = file_document.structuredContent["documents"][0]["document_uri"]
                    file_page = await client.read_resource(file_uri + "/page/1")
                    assert file_page.contents[0].text == "Independent MCP document"
                    assert file_page.contents[0].meta["text_origin"] == "pdf_text_layer"
                    escaped = await client.call_tool("ingest_document_file", {
                        "relative_path": str(source_root / "mcp-fixture.pdf"),
                    })
                    assert escaped.isError is True
                    assert escaped.structuredContent["error"]["code"] == "INVALID_ARGUMENT"

                    denied = await client.call_tool("register_wrong_answer_source", {
                        "source_uri": document_uri, "question_text": "Synthetic question",
                        "student_answer": "Synthetic answer",
                    })
                    assert denied.isError is True
                    assert denied.structuredContent["error"]["code"] == "PERMISSION_DENIED"

    anyio.run(check)
