---
tags: [prometheus-engine, fase-0, state]
---

# Fase 0 — Autonomous Loop Engine

Initialize State → Assess → Decide.

## 0a — Initialize State

```python
STATE = {
    "goal": prompt_enhanced,
    "tier": auto_detect(),
    "quality_threshold": tier_to_threshold(tier),
    "subagents_available": 100,
    "subagents_used": 0,
    "tasks_completed": [],
    "tasks_failed": [],
    "iteration": 0,
}
```

## 0b — State Assessment

Dopo ogni evento, valuta:
1. Cosa è completato?
2. Cosa è fallito?
3. Ci sono task in-flight?
4. Goal raggiungibile?
5. Devo cambiare strategia?
6. Pattern salvati per questo task?

## 0c — Decisione Autonoma

```
if tasks_in_flight:          → aspetto (streaming)
elif tasks_failed:           → retry o escalate
elif not tasks_completed:    → decompose → dispatch
elif done & quality >= soglia → COMPLETO
elif done & quality < soglia → quality improvement
```

## Collegamenti
- [[Filosofia e Core Loop]] — Il loop che governa la fase
- [[Tier System]] — Determina threshold e subagenti
- [[Fase 0.5 - Plan Integration]] — Prossimo passo per Tier 3+
- [[Fase 1 - Massive Decomposition]] — decompose_remaining()
- [[Fase 3 - Streaming Quality Gate]] — Dove arrivano i risultati
