"""
FastMCP server — wires MCP tools to renderer functions.

Contract (AGENTS.md):
- Must not contain rendering logic; delegate everything to renderer.
- Must catch all errors and return structured responses (never crash).
- Tools exposed: render_schematic, list_components, validate_spec
"""

from src.renderer import (
    CircuitSpec,
    ComponentList,
    RenderError,
    SVGString,
    ValidationResult,
    list_components as _list_components,
    render_schematic as _render_schematic,
    validate_spec as _validate_spec,
)


def create_server():
    """Create and configure the FastMCP server instance.

    Returns:
        A configured FastMCP application with all tools registered.
    """
    raise NotImplementedError


def render_schematic_tool(spec: CircuitSpec) -> dict:
    """MCP tool: render a CircuitSpec and return the SVG string.

    Delegates to renderer.render_schematic. Returns a structured dict so
    FastMCP can forward it to Claude as an artifact.
    """
    raise NotImplementedError


def list_components_tool() -> dict:
    """MCP tool: return all supported component types."""
    raise NotImplementedError


def validate_spec_tool(spec: CircuitSpec) -> dict:
    """MCP tool: validate a CircuitSpec without rendering."""
    raise NotImplementedError


def main() -> None:
    """Entry point — create and run the MCP server."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
