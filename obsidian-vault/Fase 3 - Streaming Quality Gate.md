---
tags: [prometheus-engine, fase-3, quality-gate, streaming]
---

# Fase 3 — Streaming Quality Gate

**Non aspetto. Processo subito.**

## Il Loop Streaming

```
while goal_not_achieved:
    ┌─ Arriva risultato da subagente X
    ├─ PARSE: status, quality_score, gaps, files
    ├─ VALIDATE: files esistono? (stat/check)
    │
    ├─ if score >= threshold:
    │   ├─ ✅ tasks_completed.append(X)
    │   └─ GIT CHECKPOINT: add + commit + push
    │
    ├─ if score < threshold:
    │   ├─ ❌ Retry IMMEDIATO con feedback
    │   └─ tasks_in_flight.append(X)
    │
    ├─ UPDATE: first_pass_rate, avg_quality
    └─ if ALL tasks done → 🎉 GOAL ACHIEVED
```

## Adaptive Threshold Tuning

Se FPR < 60% dopo 25% task → raddoppia granularità.
Se FPR > 90% → merge task adiacenti.

## Git Commit+Push Policy

- commit granulare dopo ogni task passato
- push immediato
- Messaggi in italiano, conventional commits

## Context Window Protection

⚠️ **Critico per Tier 3-4**: dispatcha a ondate (max 20-25), summary compressi, monitora compression trigger.

## Collegamenti
- [[Fase 2 - Autonomous Scatter]] — Da dove arrivano i risultati
- [[Fase 4 - Self-Learning Loop]] — Impara dai risultati
- [[Fase 6 - Retry Intelligence]] — Retry con feedback arricchito
- [[Fase 10 - Skill Ecosystem]] — Skill da caricare post-batch
- [[Pitfalls]] — ❌ Context window overflow
