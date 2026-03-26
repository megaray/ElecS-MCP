"""Tests for src/server.py MCP tool wrappers — AGENT: tester"""

import pytest
from src.server import list_components, render_schematic, validate_spec

RC_SPEC = {
    "version": 1,
    "elements": [
        {"type": "voltage_source", "id": "V1", "value": "5V"},
        {"type": "resistor", "id": "R1", "value": "1kΩ"},
        {"type": "ground", "id": "GND"},
    ],
}


class TestRenderSchematicTool:
    def test_success_returns_svg_key(self):
        result = render_schematic(RC_SPEC)
        assert "svg" in result
        assert "<svg" in result["svg"]

    def test_invalid_spec_returns_error_dict(self):
        result = render_schematic({"version": 1, "elements": []})
        assert "error" in result
        assert result.get("code") == "RENDER_ERROR"

    def test_never_raises(self):
        # Tool wrapper must never propagate exceptions
        result = render_schematic(None)  # type: ignore[arg-type]
        assert "error" in result or "svg" in result


class TestListComponentsTool:
    def test_returns_components_key(self):
        result = list_components()
        assert "components" in result
        assert isinstance(result["components"], list)

    def test_never_raises(self):
        result = list_components()
        assert isinstance(result, dict)


class TestValidateSpecTool:
    def test_valid_spec(self):
        result = validate_spec(RC_SPEC)
        assert result["valid"] is True

    def test_invalid_spec(self):
        result = validate_spec({"version": 1, "elements": []})
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_never_raises(self):
        result = validate_spec(None)  # type: ignore[arg-type]
        assert isinstance(result, dict)
