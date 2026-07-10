---
tags: [prometheus-engine, tier, allocation]
---

# Tier System

Il Tier system determina **quanti subagenti usare** in base alla complessità del task.

## Tabella Tier

| Fattore | T1 | T2 | T3 | T4 |
|---------|----|----|----|----|
| Files | 0-1 | 2-5 | 5-20 | 20-100+ |
| Subagenti | 0 | 1-5 | 5-30 | 10-100 |
| Soglia qualità | — | 6/10 | 7/10 | 8/10 |
| Loop autonomo | No | 1 iter | ∞ converge | ∞ converge |

## Formula Tier Detection

```python
complexity = (files_likely * 1.0) + (existing_deps * 0.5) + (has_external_apis * 2.0)

if complexity <= 2:   return 1
if complexity <= 10:  return 2
if complexity <= 40:  return 3
return 4
```

## 🧠 Fattore Familiarità

Se conosci già il codebase, riduci i subagenti:
- **Mai visto**: tabella standard
- **Esplorato**: -50%
- **Conosci a memoria**: -80% (o 0)
- **Hai scritto il modulo**: 0 subagenti

## Fast Path (Tier 1-2)

```
Tier 1: risposta diretta, nessun loop
Tier 2: decompose → dispatch → gather (max 1 retry) → report compresso
```

## Collegamenti
- [[Filosofia e Core Loop]] — Il loop che il Tier scala
- [[Fase 1 - Massive Decomposition]] — Decomposizione adattiva
- [[Fase 2 - Autonomous Scatter]] — Dispatch massivo in base al Tier
- [[Pitfalls]] — ❌ Spreco di subagenti
