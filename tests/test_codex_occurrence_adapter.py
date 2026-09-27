import base64
import json

import pytest

import chatgpt_study_system.migration.codex_occurrence_adapter as adapter_module
from chatgpt_study_system.migration.codex_occurrence_adapter import (
    CodexOccurrenceParseError,
    parse_codex_occurrence_line,
)


_SNAPSHOT = "b" * 64


def _parse(record: object, *, ordinal: int = 4) -> object:
    return parse_codex_occurrence_line(
        json.dumps(record, separators=(",", ":")).encode(),
        snapshot_sha256=_SNAPSHOT,
        source_member_ref="private/member.jsonl",
        record_ordinal=ordinal,
    )


def test_response_message_preserves_open_role_text_and_opaque_image_ref() -> None:
    private_text = "synthetic private body"
    image_data = base64.b64encode(b"synthetic image bytes").decode()
    record = {"type": "response_item", "timestamp": "raw-time-value", "payload": {
        "type": "message", "id": "source-message-id", "role": "developer",
        "content": [
            {"type": "input_text", "text": private_text},
            {"type": "input_image", "image_url": f"data:image/png;base64,{image_data}"},
        ],
    }}

    occurrence = _parse(record)

    assert occurrence.kind == "message"
    assert occurrence.role == "developer"
    assert occurrence.source_item_id == "source-message-id"
    assert occurrence.source_created_at == "raw-time-value"
    assert occurrence.conversation_ref is None
    assert occurrence.conversation_order is None
    assert occurrence.message_order is None
    assert occurrence.content_blocks[0].text == private_text
    assert occurrence.content_blocks[1].source_ref == "record:4/content:1"
    assert image_data not in repr(occurrence)


def test_event_and_unknown_record_shapes_remain_opaque_occurrences() -> None:
    event = _parse({"type": "event_msg", "payload": {"type": "task_started", "secret": "sentinel"}}, ordinal=0)
    unknown = _parse({"type": "future_record", "payload": {"private": "sentinel"}}, ordinal=1)

    assert event.kind == "task_started"
    assert event.role is None
    assert event.content_blocks[0].source_ref == "record:0"
    assert unknown.kind == "unknown_record"
    assert unknown.content_blocks[0].source_ref == "record:1"
    assert "sentinel" not in repr(event)
    assert "sentinel" not in repr(unknown)


def test_unknown_content_block_is_referenced_without_mapping_its_value() -> None:
    occurrence = _parse({"type": "response_item", "payload": {
        "type": "message", "id": "message-id", "role": "future-role",
        "content": [{"type": "future_block", "payload": "private sentinel"}],
    }})

    assert occurrence.role == "future-role"
    assert occurrence.content_blocks[0].kind == "unknown_content"
    assert occurrence.content_blocks[0].text is None
    assert occurrence.content_blocks[0].source_ref == "record:4/content:0"
    assert "private sentinel" not in repr(occurrence)


def test_unhashable_unknown_content_tags_remain_opaque() -> None:
    occurrence = _parse({"type": "response_item", "payload": {
        "type": "message", "role": "user", "content": [{"type": {"future": "tag"}}],
    }})

    assert occurrence.content_blocks[0].kind == "unknown_content"
    assert occurrence.content_blocks[0].source_ref == "record:4/content:0"


def test_parser_rejects_non_object_records_and_excess_content_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(CodexOccurrenceParseError) as error:
        parse_codex_occurrence_line(
            b"[]", snapshot_sha256=_SNAPSHOT,
            source_member_ref="private/member.jsonl", record_ordinal=0,
        )
    assert error.value.code == "unsupported_record"

    monkeypatch.setattr(adapter_module, "_MAX_CONTENT_BLOCKS", 1)
    line = json.dumps({"type": "response_item", "payload": {
        "type": "message", "content": [
            {"type": "input_text", "text": "one"},
            {"type": "output_text", "text": "two"},
        ],
    }}).encode()
    with pytest.raises(CodexOccurrenceParseError) as error:
        parse_codex_occurrence_line(
            line, snapshot_sha256=_SNAPSHOT,
            source_member_ref="private/member.jsonl", record_ordinal=0,
        )
    assert error.value.code == "content_block_limit_exceeded"


def test_malformed_oversized_and_invalid_provenance_fail_redacted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(CodexOccurrenceParseError) as error:
        parse_codex_occurrence_line(
            b"not-json", snapshot_sha256=_SNAPSHOT,
            source_member_ref="C:/private/path.jsonl", record_ordinal=0,
        )
    assert error.value.code == "malformed_json"
    assert "private" not in str(error.value)

    monkeypatch.setattr(adapter_module, "_MAX_LINE_BYTES", 2)
    with pytest.raises(CodexOccurrenceParseError) as error:
        parse_codex_occurrence_line(
            b"{}\n", snapshot_sha256=_SNAPSHOT,
            source_member_ref="C:/private/path.jsonl", record_ordinal=0,
        )
    assert error.value.code == "line_limit_exceeded"
    assert "private" not in str(error.value)

    with pytest.raises(CodexOccurrenceParseError) as error:
        parse_codex_occurrence_line(
            b"{}", snapshot_sha256="invalid private digest",
            source_member_ref="private path", record_ordinal=0,
        )
    assert error.value.code == "invalid_provenance"
    assert "private" not in str(error.value)
