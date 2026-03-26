# AGENTS.md — Claude EDA Schematic Renderer

## Project Goal

Build a MCP server that exposes schematic rendering tools to Claude, enabling inline
electronic schematic visualization directly in the Claude chat interface.
The output is an SVG/PNG rendered from a structured description of a circuit,
displayed as an artifact in the conversation.

---

## Architecture Overview

```
Claude (chat) ──MCP──> eda-schematic-server (local) ──> SchemDraw/SVG ──> image artifact
```

**Stack:**
- Python 3.11+
- `schemdraw` — schematic drawing engine
- `fastmcp` — MCP server framework
- `matplotlib` (backend for schemdraw)
- Output: SVG string returned inline, or PNG as base64

---

## Agent Roles

### AGENT: architect
**Trigger:** Any decision that changes the public MCP tool interface or the rendering pipeline.
**Responsibilities:**
- Define and freeze the MCP tool signatures (`draw_schematic`, `add_component`, etc.)
- Decide output format (SVG string vs base64 PNG vs file path)
- Validate that new features don't break existing tool contracts
- Write/update `docs/INTERFACE.md` on any change

**Must not:** Write implementation code. Only define contracts.

---

### AGENT: renderer
**Trigger:** Any task involving schemdraw, SVG generation, or visual output.
**Responsibilities:**
- Implement schematic drawing logic using schemdraw
- Map abstract component descriptions → schemdraw elements
- Handle layout (left-to-right, top-to-bottom flow)
- Produce clean, readable SVG output

**Must not:** Modify MCP server wiring or tool signatures.
**Input contract:** Receives a `CircuitSpec` dict (see `docs/INTERFACE.md`)
**Output contract:** Returns SVG string or raises `RenderError`

---

### AGENT: mcp-server
**Trigger:** Any task involving FastMCP, tool registration, or server startup.
**Responsibilities:**
- Wire MCP tools to renderer functions
- Handle input validation and error responses
- Manage server lifecycle (startup, shutdown, health)
- Write/update `docs/SERVER.md`

**Must not:** Contain rendering logic. Delegate everything to `renderer`.

---

### AGENT: tester
**Trigger:** Any new component type, tool signature change, or bug report.
**Responsibilities:**
- Write pytest tests for each MCP tool
- Test edge cases: empty circuit, unknown component, malformed input
- Validate SVG output is non-empty and parseable
- Maintain `tests/` directory

**Must not:** Modify source code. Only write tests and report failures.

---

### AGENT: integrator
**Trigger:** End-to-end testing with Claude Desktop or claude.ai artifacts.
**Responsibilities:**
- Write the `claude_desktop_config.json` snippet
- Document how to install and connect the MCP server
- Test the full loop: Claude prompt → MCP call → SVG rendered in chat
- Write/update `README.md`

**Must not:** Change server or renderer internals.

---

## Context Anchors

These files are the source of truth. Read them before any task.
Changing them requires explicit user confirmation.

| File | Purpose |
|------|---------|
| `docs/INTERFACE.md` | MCP tool signatures + CircuitSpec schema |
| `docs/COMPONENTS.md` | Supported component types + schemdraw mapping |
| `src/renderer.py` | Core rendering logic |
| `src/server.py` | MCP server entry point |
| `AGENTS.md` | This file — agent roles and constraints |

---

## CircuitSpec Schema (v1)

This is the canonical input format. Do not change without updating `docs/INTERFACE.md`
and bumping the version.

```json
{
  "version": 1,
  "title": "RC Low-pass Filter",
  "elements": [
    { "type": "voltage_source", "id": "V1", "value": "5V", "at": "start" },
    { "type": "resistor",       "id": "R1", "value": "1kΩ" },
    { "type": "capacitor",      "id": "C1", "value": "10µF", "to": "ground" },
    { "type": "ground",         "id": "GND" }
  ],
  "style": "IEC"
}
```

**Supported styles:** `"IEC"` (EU rectangles), `"ANSI"` (US zigzag)

---

## MCP Tool Signatures (v1)

Defined by `architect`. Do not modify without architect sign-off.

### `render_schematic(spec: CircuitSpec) -> SVGString`
Renders a full circuit from a CircuitSpec. Returns SVG as a string.

### `list_components() -> ComponentList`
Returns all supported component types with their schemdraw mapping.

### `validate_spec(spec: CircuitSpec) -> ValidationResult`
Validates a CircuitSpec without rendering. Returns errors/warnings.

---

## Constraints & Guardrails

- **No agent modifies files outside its scope** (see "Must not" per agent above)
- **Interface changes require a version bump** in CircuitSpec and tool signatures
- **Rendering must be stateless** — no session state in the server
- **All errors must be caught** — never crash the MCP server, return structured errors
- **SVG output must be self-contained** — no external font or asset dependencies

---

## Development Phases

### Phase 1 — MVP (current)
- [ ] `render_schematic` for series circuits (R, C, L, V source, GND)
- [ ] SVG output returned inline
- [ ] FastMCP server running locally
- [ ] Works with Claude Desktop

### Phase 2 — Component Library
- [ ] Transistors (NPN, PNP, MOSFET)
- [ ] Op-amps
- [ ] Diodes, LEDs, Zeners
- [ ] IC blocks (generic DIP)

### Phase 3 — Layout Intelligence
- [ ] Automatic branch detection (parallel components)
- [ ] Net labels
- [ ] Multi-sheet / sub-circuits

### Phase 4 — Claude.ai Integration
- [ ] Hosted MCP endpoint (not just local)
- [ ] Base64 PNG returned as artifact

---
