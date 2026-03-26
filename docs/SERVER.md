# SERVER.md — MCP Server Operations

> Maintained by **AGENT: mcp-server**.

---

## Transports

The server supports two transports selected via the `--transport` flag.

| Flag | Protocol | Use case |
|------|----------|----------|
| `--transport stdio` | stdin/stdout | Claude Desktop (local, default) |
| `--transport http` | HTTP + SSE | Remote deployment (Raspberry Pi, LAN) |

---

## Running locally (Claude Desktop)

```bash
python -m src.server
# or explicitly:
python -m src.server --transport stdio
```

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or the equivalent path on your OS:

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

See [`docs/claude_desktop_config.json`](claude_desktop_config.json) for a
ready-to-paste snippet.

---

## Running remotely (Raspberry Pi / LAN)

```bash
python -m src.server --transport http            # binds 0.0.0.0:8000
python -m src.server --transport http --port 9000
```

The server listens on **all interfaces** (`0.0.0.0`) so it is reachable from
other machines on the same network.

### Connecting Claude Desktop to a remote server

```json
{
  "mcpServers": {
    "elecs-mcp-remote": {
      "url": "http://<raspberry-pi-ip>:8000/sse"
    }
  }
}
```

### Running as a systemd service (Raspberry Pi)

```ini
# /etc/systemd/system/elecs-mcp.service
[Unit]
Description=ElecS MCP schematic server
After=network.target

[Service]
ExecStart=/usr/local/bin/python3 -m src.server --transport http --port 8000
WorkingDirectory=/home/pi/ElecS-MCP
Restart=on-failure
Environment=MPLBACKEND=Agg

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now elecs-mcp
sudo systemctl status elecs-mcp
```

---

## CLI reference

```
usage: elecs-mcp [-h] [--transport {stdio,http}] [--port PORT]

options:
  --transport {stdio,http}   Transport protocol (default: stdio)
  --port PORT                Port for HTTP transport (default: 8000)
```

---

## Health check (HTTP transport only)

FastMCP does not expose a dedicated `/health` endpoint, but a quick
connectivity check can confirm the server is up:

```bash
curl -i http://<host>:<port>/sse
# expected: HTTP 200 with Content-Type: text/event-stream
```

---

## Environment variables

| Variable | Effect |
|----------|--------|
| `MPLBACKEND` | Set to `Agg` to force headless matplotlib (required on Pi without display) |
| `FASTMCP_PORT` | Overrides default port (fastmcp built-in) |
| `FASTMCP_HOST` | Overrides bind host (fastmcp built-in) |
