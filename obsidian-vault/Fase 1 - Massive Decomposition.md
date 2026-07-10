---
tags: [prometheus-engine, fase-1, decompose, clean-code]
---

# Fase 1 — Massive Parallel Decomposition

Decomposizione dinamica, non fissa. Include [[Phase 1d-bis - Clean Code Standards|Clean Code Standards]] per Tier 2-4.

## Decomposizione Adattiva

```python
def decompose(goal, available_subagents, iteration):
    safe_iteration = max(0, iteration)
    if safe_iteration == 0:
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

Prima di dispatchare subagenti che producono moduli comunicanti, documenta le **firme complete** delle funzioni condivise nel context di ENTRAMBI. **Attenzione:** con dispatch dinamico, Batch 2 si adatta alle firme già scritte da Batch 1.

## Quality Criteria Dinamici

Ogni task riceve criteri adattivi per tipo (api, model, ui). Vedi [[Fase 1 - Massive Decomposition#1d-bis|1d-bis]] per i nuovi criteri Clean Code.

## 1d-bis — Clean Code Standards (per Tier)

Vedi [[Phase 1d-bis - Clean Code Standards]] per i dettagli.

- **Tier 2-4:** Type Hints + Docstrings obbligatori (verificabili)
- **Tier 3-4:** SRP via Actor-Critic (solo dopo 3+ retry)
- **Tier 3-4:** DRY via Assembly Task (post-batch)

## Collegamenti
- [[Tier System]] — Determina quanti subagenti
- [[Fase 0.5 - Plan Integration]] — Piano che alimenta la decomposizione
- [[Fase 2 - Autonomous Scatter]] — Dispatch dei task decomposti
- [[Phase 1d-bis - Clean Code Standards]] — Criteri Clean Code
- [[Pitfalls]] — ❌ Decomposizione non adattiva
