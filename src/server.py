"""
FastMCP server — wires MCP tools to renderer functions.

Contract (AGENTS.md):
- Must not contain rendering logic; delegate everything to renderer.
- Must catch all errors and return structured responses (never crash).
- Tools exposed: render_schematic, list_components, validate_spec
"""

from __future__ import annotations

from fastmcp import FastMCP

from src.renderer import (
    CircuitSpec,
    RenderError,
    list_components as _list_components,
    render_schematic as _render_schematic,
    validate_spec as _validate_spec,
)

mcp = FastMCP(
    name="elecs-mcp",
    version="0.1.0",
    instructions=(
        "Render electronic schematics from a structured CircuitSpec. "
        "Use render_schematic to get an SVG, list_components to see supported "
        "parts, or validate_spec to check a spec before rendering."
    ),
)


@mcp.tool()
def render_schematic(spec: dict) -> dict:
    """Render a full circuit from a CircuitSpec and return the SVG string.

    Args:
        spec: A CircuitSpec v1 object (see docs/INTERFACE.md).

    Returns:
        On success: {"svg": "<svg ...>"}
        On failure: {"error": "...", "code": "RENDER_ERROR"}
    """
    try:
        svg = _render_schematic(spec)
        return {"svg": svg}
    except RenderError as exc:
        return {"error": str(exc), "code": "RENDER_ERROR"}
    except Exception as exc:
        return {"error": f"Unexpected error: {exc}", "code": "INTERNAL_ERROR"}


@mcp.tool()
def list_components() -> dict:
    """Return all supported component types with their SchemDraw mapping.

    Returns:
        {"components": [{type, schemdraw_class, description}, ...]}
    """
    try:
        return {"components": _list_components()}
    except Exception as exc:
        return {"error": f"Unexpected error: {exc}", "code": "INTERNAL_ERROR"}


@mcp.tool()
def validate_spec(spec: dict) -> dict:
    """Validate a CircuitSpec without rendering.

    Args:
        spec: A CircuitSpec v1 object to validate.

    Returns:
        {"valid": bool, "errors": [...], "warnings": [...]}
    """
    try:
        return _validate_spec(spec)
    except Exception as exc:
        return {"error": f"Unexpected error: {exc}", "code": "INTERNAL_ERROR"}


def main() -> None:
    """Entry point — run the MCP server over stdio (default for Claude Desktop)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
