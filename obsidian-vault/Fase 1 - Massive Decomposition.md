---
tags: [prometheus-engine, fase-1, decompose]
---

# Fase 1 — Massive Parallel Decomposition

Decomposizione dinamica, non fissa.

## Decomposizione Adattiva

```python
def decompose(goal, available_subagents, iteration):
    if iteration == 0:
        return fine_grained_decompose(goal, count=available * 0.8)
    else:
        return fine_grained_decompose(gaps, count=len(gaps) * 3)
```

## Regole di Scala

| Subagenti | Pattern |
|-----------|---------|
| 1-5 | Task per file |
| 5-15 | Task per funzione |
| 15-50 | Task per sotto-componente |
| 50-100 | Task per riga logica + varianti |

## Interface Contracts (pre-dispatch)

Prima di dispatchare subagenti che producono moduli comunicanti, documenta le **firme complete** delle funzioni condivise nel context di ENTRAMBI.

**Esempio:**
```
--- CONTRATTO INTERFACCIA ---
build_prompt(location, target_date, sources, ...) -> str
  SINCRONA

call_ollama(prompt, max_retries=3) -> OllamaForecast
  ASINCRONA
--- FINE CONTRATTO ---
```

## Quality Criteria Dinamici

Ogni task riceve criteri adattivi per tipo (api, model, ui).

## Collegamenti
- [[Tier System]] — Determina quanti subagenti
- [[Fase 0.5 - Plan Integration]] — Piano che alimenta la decomposizione
- [[Fase 2 - Autonomous Scatter]] — Dispatch dei task decomposti
- [[Pitfalls]] — ❌ Decomposizione non adattiva
