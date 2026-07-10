---
tags: [prometheus-engine, pattern, precision, float, polymarket]
---

# Int-to-Float Precision

Convertire tutto lo stack da int a 1 decimale per Polymarket betting.

## Perché
I mercati Polymarket risolvono al **decimo di grado** (es. 34.1°C). Arrotondare a interi perde informazione preziosa per il betting.

## Cosa è stato cambiato

| Layer | Prima | Ora |
|-------|-------|-----|
| Schemas Pydantic | `Optional[int]` | `Optional[float]` |
| DB SQLAlchemy | `Integer` | `Float` |
| Weather fetcher | `_int(value)` | `_float(value)` → `round(x, 1)` |
| Climatologia | `round(x)` | `round(x, 1)` |
| Prompt AI | "34°C" | "34.3°C" |
| Frontend | `Math.round()` | `.toFixed(1)` |
| Fasce probabilità | "30-32°C" | "30.5-31.4°C" |

## Collegamenti
- [[Ensemble Confidence Scoring]] — Confidence usa float
- [[Climatology 3 Levels]] — Climato con 1 decimale
- [[AI Response Caching]] — Cache con float
- [[Pitfalls]] — ❌ Precisione floating point
