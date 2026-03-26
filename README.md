# ElecS-MCP — Electronic Schematic Renderer for Claude

An MCP server that lets Claude render electronic schematics inline in the chat
interface. Describe a circuit as a JSON object; get back a self-contained SVG.

```
Claude (chat) ──MCP──> elecs-mcp (local) ──> SchemDraw ──> SVG artifact
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/megaray/ElecS-MCP.git
cd ElecS-MCP
pip install -e ".[dev]"
```

### 2. Connect to Claude Desktop

Add the following to your `claude_desktop_config.json`
(see [`docs/claude_desktop_config.json`](docs/claude_desktop_config.json) for a ready-to-paste snippet):

```json
{
  "mcpServers": {
    "elecs-mcp": {
      "command": "/usr/local/bin/python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/ElecS-MCP"
    }
  }
}
```

Restart Claude Desktop. You should see **elecs-mcp** listed under connected MCP servers.

### 3. Ask Claude to draw a circuit

```
Draw me an RC low-pass filter with a 1kΩ resistor and 10µF capacitor.
```

Claude will call `render_schematic` and display the SVG directly in the chat.

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `render_schematic(spec)` | Render a CircuitSpec → SVG string |
| `list_components()` | List all supported component types |
| `validate_spec(spec)` | Validate a CircuitSpec without rendering |

Full signatures: [`docs/INTERFACE.md`](docs/INTERFACE.md)

---

## CircuitSpec Format

```json
{
  "version": 1,
  "title": "RC Low-pass Filter",
  "elements": [
    { "type": "voltage_source", "id": "V1", "value": "5V" },
    { "type": "resistor",       "id": "R1", "value": "1kΩ" },
    { "type": "capacitor",      "id": "C1", "value": "10µF" },
    { "type": "ground",         "id": "GND" }
  ],
  "style": "IEC"
}
```

**Supported styles:** `"IEC"` (EU rectangles, default) · `"ANSI"` (US zigzag)

**Supported component types:** resistor, capacitor, inductor, voltage_source, ground, wire

Full component list: [`docs/COMPONENTS.md`](docs/COMPONENTS.md)

---

## Development

```bash
# Run tests
python -m pytest tests/ -v

# Run the server manually (stdio transport)
python -m src.server
```

---

## Stack

- Python 3.11+
- [`schemdraw`](https://schemdraw.readthedocs.io/) — schematic drawing engine
- [`fastmcp`](https://github.com/jlowin/fastmcp) — MCP server framework
- `matplotlib` — headless rendering backend

---

## Roadmap

See [`AGENTS.md`](AGENTS.md) for development phases and agent roles.

- **Phase 1 (current):** Series circuits — R, C, L, voltage source, GND
- **Phase 2:** Transistors, op-amps, diodes, ICs
- **Phase 3:** Parallel branches, net labels, sub-circuits
- **Phase 4:** Hosted endpoint, PNG artifacts for claude.ai
