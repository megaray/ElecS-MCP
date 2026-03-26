# INTERFACE.md — MCP Tool Signatures & CircuitSpec Schema

> Maintained by **AGENT: architect**. Any change requires a version bump and
> explicit user confirmation before merging.

---

## CircuitSpec Schema — v1

```json
{
  "version": 1,
  "title": "string (optional)",
  "elements": [
    {
      "type": "string",   // required — see docs/COMPONENTS.md
      "id":   "string",   // required — unique within the circuit
      "value":"string",   // optional — e.g. "1kΩ", "10µF"
      "at":   "string",   // optional — layout hint, e.g. "start"
      "to":   "string"    // optional — layout hint, e.g. "ground"
    }
  ],
  "style": "IEC | ANSI"   // optional, default "IEC"
}
```

**Rules:**
- `version` must equal `1` for v1 processing.
- `elements` must be a non-empty array.
- Each element must have a unique `id`.
- Unknown `type` values cause a `RenderError`.

---

## Tool Signatures — v1

### `render_schematic(spec: CircuitSpec) -> SVGString`

Renders a full circuit from a CircuitSpec.

| Parameter | Type         | Required | Description                  |
|-----------|--------------|----------|------------------------------|
| `spec`    | CircuitSpec  | yes      | v1 circuit description       |

**Returns:** Self-contained SVG string (no external assets).
**Errors:** Returns structured error dict `{error: str, code: str}` on failure.

---

### `list_components() -> ComponentList`

Returns all supported component types.

**Returns:** Array of objects:

```json
[
  {
    "type": "resistor",
    "schemdraw_class": "elm.Resistor",
    "description": "Resistor (ANSI zigzag / IEC rectangle)"
  }
]
```

---

### `validate_spec(spec: CircuitSpec) -> ValidationResult`

Validates a CircuitSpec without rendering.

| Parameter | Type        | Required | Description            |
|-----------|-------------|----------|------------------------|
| `spec`    | CircuitSpec | yes      | v1 circuit description |

**Returns:**

```json
{
  "valid":    true,
  "errors":   [],
  "warnings": []
}
```

`valid` is `false` if any `errors` are present. `warnings` are non-fatal.
