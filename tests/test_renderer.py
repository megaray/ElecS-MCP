"""Tests for src/renderer.py — AGENT: tester"""

import pytest
from src.renderer import (
    RenderError,
    list_components,
    render_schematic,
    validate_spec,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

RC_SPEC = {
    "version": 1,
    "title": "RC Low-pass Filter",
    "elements": [
        {"type": "voltage_source", "id": "V1", "value": "5V"},
        {"type": "resistor", "id": "R1", "value": "1kΩ"},
        {"type": "capacitor", "id": "C1", "value": "10µF"},
        {"type": "ground", "id": "GND"},
    ],
    "style": "IEC",
}


# ---------------------------------------------------------------------------
# validate_spec
# ---------------------------------------------------------------------------

class TestValidateSpec:
    def test_valid_rc_circuit(self):
        result = validate_spec(RC_SPEC)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_missing_version(self):
        spec = {**RC_SPEC}
        del spec["version"]  # type: ignore[misc]
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("version" in e for e in result["errors"])

    def test_wrong_version(self):
        result = validate_spec({**RC_SPEC, "version": 99})
        assert result["valid"] is False
        assert any("unsupported version" in e for e in result["errors"])

    def test_missing_elements(self):
        spec = {"version": 1}
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("elements" in e for e in result["errors"])

    def test_empty_elements(self):
        result = validate_spec({"version": 1, "elements": []})
        assert result["valid"] is False
        assert any("empty" in e for e in result["errors"])

    def test_unknown_component_type(self):
        spec = {
            "version": 1,
            "elements": [{"type": "flux_capacitor", "id": "FC1"}],
        }
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("flux_capacitor" in e for e in result["errors"])

    def test_duplicate_ids(self):
        spec = {
            "version": 1,
            "elements": [
                {"type": "resistor", "id": "R1"},
                {"type": "capacitor", "id": "R1"},
            ],
        }
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("duplicate" in e for e in result["errors"])

    def test_missing_element_id(self):
        spec = {"version": 1, "elements": [{"type": "resistor"}]}
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("id" in e for e in result["errors"])

    def test_unknown_style_is_warning(self):
        spec = {**RC_SPEC, "style": "SPICE"}
        result = validate_spec(spec)
        assert result["valid"] is True  # not fatal
        assert any("style" in w for w in result["warnings"])

    def test_not_a_dict(self):
        result = validate_spec("not a dict")  # type: ignore[arg-type]
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# list_components
# ---------------------------------------------------------------------------

class TestListComponents:
    def test_returns_list(self):
        components = list_components()
        assert isinstance(components, list)
        assert len(components) > 0

    def test_each_entry_has_required_keys(self):
        for comp in list_components():
            assert "type" in comp
            assert "schemdraw_class" in comp
            assert "description" in comp

    def test_phase1_components_present(self):
        types = {c["type"] for c in list_components()}
        for expected in ("resistor", "capacitor", "inductor", "voltage_source", "ground", "wire"):
            assert expected in types, f"missing component type: {expected}"


# ---------------------------------------------------------------------------
# render_schematic
# ---------------------------------------------------------------------------

class TestRenderSchematic:
    def test_rc_circuit_returns_svg(self):
        svg = render_schematic(RC_SPEC)
        assert isinstance(svg, str)
        assert len(svg) > 0
        assert "<svg" in svg

    def test_svg_is_self_contained(self):
        svg = render_schematic(RC_SPEC)
        # No external resource references
        assert "http://" not in svg or "www.w3.org" in svg  # only W3C namespaces allowed
        assert "src=" not in svg

    def test_single_resistor(self):
        spec = {"version": 1, "elements": [{"type": "resistor", "id": "R1", "value": "100Ω"}]}
        svg = render_schematic(spec)
        assert "<svg" in svg

    def test_invalid_spec_raises_render_error(self):
        with pytest.raises(RenderError):
            render_schematic({"version": 1, "elements": []})

    def test_unknown_type_raises_render_error(self):
        spec = {
            "version": 1,
            "elements": [{"type": "unknown_part", "id": "X1"}],
        }
        with pytest.raises(RenderError):
            render_schematic(spec)

    def test_all_phase1_types_render(self):
        spec = {
            "version": 1,
            "elements": [
                {"type": "voltage_source", "id": "V1", "value": "5V"},
                {"type": "resistor", "id": "R1", "value": "1kΩ"},
                {"type": "capacitor", "id": "C1", "value": "10µF"},
                {"type": "inductor", "id": "L1", "value": "10mH"},
                {"type": "ground", "id": "GND"},
            ],
        }
        svg = render_schematic(spec)
        assert "<svg" in svg
