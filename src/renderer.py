"""
Schematic rendering logic using SchemDraw.

Contract (AGENTS.md):
- Input:  CircuitSpec dict (see docs/INTERFACE.md)
- Output: SVG string, or raises RenderError
- Must be stateless — no session state retained between calls
"""

from typing import Any


class RenderError(Exception):
    """Raised when a CircuitSpec cannot be rendered."""


# Type aliases (kept simple to avoid runtime deps at import time)
CircuitSpec = dict[str, Any]
SVGString = str
ComponentList = list[dict[str, Any]]
ValidationResult = dict[str, Any]


def render_schematic(spec: CircuitSpec) -> SVGString:
    """Render a full circuit from a CircuitSpec and return SVG as a string.

    Args:
        spec: A CircuitSpec dict conforming to the v1 schema in docs/INTERFACE.md.

    Returns:
        A self-contained SVG string.

    Raises:
        RenderError: If the spec is invalid or rendering fails.
    """
    raise NotImplementedError


def list_components() -> ComponentList:
    """Return all supported component types with their SchemDraw mapping.

    Returns:
        List of dicts, each with keys: type, schemdraw_class, description.
    """
    raise NotImplementedError


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
    raise NotImplementedError
