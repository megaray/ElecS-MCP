"""
Schematic rendering logic using SchemDraw.

Contract (AGENTS.md):
- Input:  CircuitSpec dict (see docs/INTERFACE.md)
- Output: SVG string, or raises RenderError
- Must be stateless — no session state retained between calls
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # headless — must be set before any other matplotlib import

import schemdraw
import schemdraw.elements as elm

from typing import Any

# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

CircuitSpec = dict[str, Any]
SVGString = str
ComponentList = list[dict[str, Any]]
ValidationResult = dict[str, Any]

# ---------------------------------------------------------------------------
# Component registry
# ---------------------------------------------------------------------------

# Maps CircuitSpec element type → (schemdraw class, human description)
_COMPONENT_MAP: dict[str, tuple[type, str]] = {
    "resistor":       (elm.Resistor,  "Resistor (ANSI zigzag / IEC rectangle)"),
    "capacitor":      (elm.Capacitor, "Capacitor"),
    "inductor":       (elm.Inductor,  "Inductor / coil"),
    "voltage_source": (elm.SourceV,   "Ideal voltage source"),
    "ground":         (elm.Ground,    "Ground reference"),
    "wire":           (elm.Line,      "Plain conductor segment"),
}

# Direction sequence for a simple series loop (down the right side, back left)
_SERIES_DIRECTIONS = ["up", "right", "down", "left"]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class RenderError(Exception):
    """Raised when a CircuitSpec cannot be rendered."""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_schematic(spec: CircuitSpec) -> SVGString:
    """Render a full circuit from a CircuitSpec and return SVG as a string.

    Args:
        spec: A CircuitSpec dict conforming to the v1 schema in docs/INTERFACE.md.

    Returns:
        A self-contained SVG string.

    Raises:
        RenderError: If the spec is invalid or rendering fails.
    """
    result = validate_spec(spec)
    if not result["valid"]:
        raise RenderError("; ".join(result["errors"]))

    elements = spec["elements"]

    try:
        d = schemdraw.Drawing(canvas="svg")

        # Simple heuristic layout: place elements in sequence, cycling through
        # up → right → down → left to form a closed loop.
        dir_cycle = _SERIES_DIRECTIONS
        dir_idx = 0

        for elem in elements:
            etype = elem["type"]

            if etype == "ground":
                # Ground anchors to current position; no direction advance.
                d += elm.Ground()
                continue

            cls = _COMPONENT_MAP[etype][0]
            el = cls()

            direction = dir_cycle[dir_idx % len(dir_cycle)]
            el = getattr(el, direction)()
            dir_idx += 1

            # Build label: id first, then value if present
            label_parts = [elem["id"]]
            if elem.get("value"):
                label_parts.append(elem["value"])
            el = el.label("\n".join(label_parts))

            d += el

        svg_bytes: bytes = d.get_imagedata("svg")
        return svg_bytes.decode("utf-8")

    except RenderError:
        raise
    except Exception as exc:
        raise RenderError(f"Rendering failed: {exc}") from exc


def list_components() -> ComponentList:
    """Return all supported component types with their SchemDraw mapping.

    Returns:
        List of dicts, each with keys: type, schemdraw_class, description.
    """
    return [
        {
            "type": name,
            "schemdraw_class": f"elm.{cls.__name__}",
            "description": desc,
        }
        for name, (cls, desc) in _COMPONENT_MAP.items()
    ]


def validate_spec(spec: CircuitSpec) -> ValidationResult:
    """Validate a CircuitSpec without rendering.

    Args:
        spec: A CircuitSpec dict to validate.

    Returns:
        Dict with keys:
            valid (bool): True if the spec is renderable.
            errors (list[str]): Fatal issues preventing rendering.
            warnings (list[str]): Non-fatal issues.
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(spec, dict):
        errors.append("spec must be a JSON object")
        return {"valid": False, "errors": errors, "warnings": warnings}

    # version
    version = spec.get("version")
    if version is None:
        errors.append("missing required field: version")
    elif version != 1:
        errors.append(f"unsupported version: {version!r} (only version 1 is supported)")

    # elements
    elements = spec.get("elements")
    if elements is None:
        errors.append("missing required field: elements")
    elif not isinstance(elements, list):
        errors.append("elements must be an array")
    elif len(elements) == 0:
        errors.append("elements must not be empty")
    else:
        seen_ids: set[str] = set()
        for i, elem in enumerate(elements):
            if not isinstance(elem, dict):
                errors.append(f"elements[{i}] must be an object")
                continue

            eid = elem.get("id")
            if not eid:
                errors.append(f"elements[{i}] missing required field: id")
            elif eid in seen_ids:
                errors.append(f"duplicate element id: {eid!r}")
            else:
                seen_ids.add(eid)

            etype = elem.get("type")
            if not etype:
                errors.append(f"elements[{i}] missing required field: type")
            elif etype not in _COMPONENT_MAP:
                errors.append(
                    f"unknown component type {etype!r} in element {eid!r}; "
                    f"supported: {', '.join(_COMPONENT_MAP)}"
                )

    # style
    style = spec.get("style")
    if style is not None and style not in ("IEC", "ANSI"):
        warnings.append(f"unknown style {style!r}; defaulting to IEC")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
