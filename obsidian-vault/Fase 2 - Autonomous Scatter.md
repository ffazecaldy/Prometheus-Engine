---
tags: [prometheus-engine, fase-2, scatter, dispatch]
---

# Fase 2 — Autonomous Scatter

Dispatch massivo in parallelo con streaming.

## Streaming Dispatch

```
┌─ Decomponi in 50 task
├─ Dispatch BATCH 1: task 1-25
├─ Mentre BATCH 1 gira:
│   ├─ Prepara BATCH 2: task 26-50
│   ├─ Valuta SUBITO ogni risultato
│   │   ├─ pass? ✅ done
│   │   └─ fail? ❌ retry IMMEDIATO
│   ├─ Dispatch BATCH 2
│   └─ Retry si mischiano naturalmente
```

## Pre-Flight Checklist

- [ ] Ogni task ha file diverso? (nessun conflitto)
- [ ] Quality criteria specifici?
- [ ] Carico bilanciato?
- [ ] Firma interfacce in entrambi i context?
- [ ] Template di retry pronti?

## Subagent Prompt Template

Ogni subagente sa di far parte di un loop più grande: riceve task_id, soglia qualità, quality criteria, e l'istruzione **"Ritorna summary CONCISO"**.

## Collegamenti
- [[Fase 1 - Massive Decomposition]] — Cosa viene dispatchato
- [[Fase 3 - Streaming Quality Gate]] — Dove arrivano i risultati
- [[Pitfalls]] — ❌ Streaming gather dimenticato
- [[Fase 5 - Scale Patterns]] — Pattern per 100 subagenti
