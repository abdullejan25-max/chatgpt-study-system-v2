"""Synthetic MCP clients share Gateway state across independent process restarts."""

import anyio
import json
import os
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from chatgpt_study_system.adapters.documents import DocumentInput, SQLiteDocumentStore


def test_independent_stdio_clients_share_workflow_and_versioned_gateway_state(tmp_path: Path) -> None:
    study = tmp_path / "study"
    assets = tmp_path / "assets"
    study.mkdir()
    assets.mkdir()
    (study / "fractions.md").write_text("# Fractions\nSynthetic reference", encoding="utf-8")

    asset_database = tmp_path / "assets.db"
    document = SQLiteDocumentStore(assets, asset_database).ingest_documents([
        DocumentInput(
            "Synthetic parity source", "text/plain", b"Synthetic source evidence",
            None, None,
        ),
    ])[0]

    config = tmp_path / "runtime.toml"
    config.write_text(
        '[gateway]\nversion="0.1.0"\n[study]\n'
        f'root={json.dumps(study.as_posix())}\nqmd_collection="studyvault"\n'
        'qmd_version="2.8.3"\nqmd_executable="synthetic-qmd-not-installed"\n'
        '[history]\nbackend="not_configured"\n'
        '[assets]\nbackend="sqlite"\n'
        f'root={json.dumps(assets.as_posix())}\n'
        f'database={json.dumps(asset_database.as_posix())}\n'
        '[permissions]\ncapabilities=["read", "write"]\n',
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

    async def run_client(operation):
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as client:
                await client.initialize()
                tools = {tool.name: tool for tool in (await client.list_tools()).tools}
                workflow_resource = next(
                    resource for resource in (await client.list_resources()).resources
                    if str(resource.uri) == "study-workflow://wrong-answer"
                )
                workflow = (await client.read_resource(str(workflow_resource.uri))).contents[0].text
                return await operation(client, tools, workflow)

    source_state: dict[str, object] = {}

    async def client_a_writes(client, tools, workflow):
        required = {
            "register_wrong_answer_source", "get_wrong_answer_bundle", "search_wrong_answers",
            "save_wrong_answer_analysis", "update_wrong_answer_analysis",
        }
        assert required <= set(tools)
        assert "explicit request to save" in workflow.lower()
        registered = await client.call_tool("register_wrong_answer_source", {
            "source_uri": document.uri,
            "question_text": "Synthetic parity question: add 1/2 and 1/3.",
            "student_answer": "2/5",
            "provenance": {"reported_agent": "SyntheticClientA", "reported_client": "stdio-test"},
        })
        source = registered.structuredContent["source"]
        source_state["source_id"] = source["source_id"]
        source_state["workflow"] = workflow
        saved = await client.call_tool("save_wrong_answer_analysis", {
            "source_id": source["source_id"],
            "analysis": {
                "error_type": "denominator",
                "knowledge_points": ["fraction addition"],
                "reasoning": "Synthetic client A analysis.",
                "correct_solution": "3/6 + 2/6 = 5/6.",
                "review_advice": "Practice a second synthetic sum.",
            },
            "source_refs": [document.uri],
            "study_relations": ["study:fractions.md"],
            "idempotency_key": "synthetic-client-a-v1",
            "expected_version": 0,
            "provenance": {"reported_agent": "SyntheticClientA", "reported_client": "stdio-test"},
        })
        first = saved.structuredContent["analysis"]
        assert first["version"] == 1
        assert first["write_provenance"]["identity_trust"] == "reported"
        source_state["analysis_v1_id"] = first["analysis_id"]
        return set(tools)

    async def client_b_reads_and_updates(client, tools, workflow):
        assert set(tools) == source_state["tool_names"]
        assert workflow == source_state["workflow"]
        fetched = await client.call_tool("get_wrong_answer_bundle", {
            "source_id": source_state["source_id"],
        })
        bundle = fetched.structuredContent["bundle"]
        assert bundle["source"]["source_id"] == source_state["source_id"]
        assert [analysis["version"] for analysis in bundle["analyses"]] == [1]

        searched = await client.call_tool("search_wrong_answers", {"query": "parity question"})
        assert any(row["source_id"] == source_state["source_id"]
                   for row in searched.structuredContent["results"])

        update_arguments = {
            "source_id": source_state["source_id"],
            "analysis": {
                "error_type": "denominator",
                "knowledge_points": ["fraction addition"],
                "reasoning": "Synthetic client B follow-up.",
                "correct_solution": "3/6 + 2/6 = 5/6.",
                "review_advice": "Practice one more synthetic sum.",
            },
            "source_refs": [document.uri],
            "study_relations": ["study:fractions.md"],
            "idempotency_key": "synthetic-client-b-v2",
            "expected_version": 1,
            "provenance": {"reported_agent": "SyntheticClientB", "reported_client": "stdio-test"},
        }
        updated = await client.call_tool("update_wrong_answer_analysis", update_arguments)
        second = updated.structuredContent["analysis"]
        assert second["version"] == 2
        assert second["supersedes_analysis_id"] == source_state["analysis_v1_id"]
        assert second["write_provenance"]["reported_agent"] == "SyntheticClientB"
        assert second["write_provenance"]["identity_trust"] == "reported"

        replay = await client.call_tool("update_wrong_answer_analysis", update_arguments)
        assert replay.structuredContent["analysis"]["analysis_id"] == second["analysis_id"]
        assert replay.structuredContent["analysis"]["version"] == 2

        stale = await client.call_tool("update_wrong_answer_analysis", {
            **update_arguments,
            "idempotency_key": "synthetic-client-b-stale-v1",
        })
        assert stale.isError is True
        assert stale.structuredContent["error"]["code"] == "CONFLICT"

    async def client_a_reads_after_restart(client, tools, workflow):
        assert set(tools) == source_state["tool_names"]
        assert workflow == source_state["workflow"]
        fetched = await client.call_tool("get_wrong_answer_bundle", {
            "source_id": source_state["source_id"],
        })
        versions = {analysis["version"]: analysis for analysis in
                    fetched.structuredContent["bundle"]["analyses"]}
        assert set(versions) == {1, 2}
        assert versions[2]["supersedes_analysis_id"] == versions[1]["analysis_id"]
        assert versions[2]["review_advice"] == "Practice one more synthetic sum."

    async def check() -> None:
        with anyio.fail_after(90):
            source_state["tool_names"] = await run_client(client_a_writes)
            await run_client(client_b_reads_and_updates)
            await run_client(client_a_reads_after_restart)

    anyio.run(check)
