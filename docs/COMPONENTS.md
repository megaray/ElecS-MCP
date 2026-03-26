# COMPONENTS.md — Supported Component Types

> Maintained by **AGENT: renderer**. Update when adding new component mappings.

---

## Phase 1 — MVP Components

| type             | SchemDraw class      | Notes                        |
|------------------|----------------------|------------------------------|
| `resistor`       | `elm.Resistor`       | Style-aware: ANSI/IEC        |
| `capacitor`      | `elm.Capacitor`      |                              |
| `inductor`       | `elm.Inductor`       |                              |
| `voltage_source` | `elm.SourceV`        |                              |
| `ground`         | `elm.Ground`         |                              |
| `wire`           | `elm.Line`           | Plain conductor segment      |

---

## Phase 2 — Planned

- `transistor_npn`, `transistor_pnp`
- `mosfet_n`, `mosfet_p`
- `opamp`
- `diode`, `led`, `zener`
- `ic_dip`
