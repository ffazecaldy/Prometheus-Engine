---
tags: [prometheus-engine, fase-3, quality-gate, streaming, security, execution]
---

# Fase 3 — Streaming Quality Gate

**Non aspetto. Processo subito.**

## Pipeline di Validazione Completa

```
while goal_not_achieved:
    ┌─ Arriva risultato da subagente X
    ├─ PARSE: status, quality_score, gaps, files
    ├─ VALIDATE (Phase 3d): files esistono sul disco?
    ├─ EXECUTION (Phase 3d-bis): codice compila/gira in sandbox?
    ├─ SECURITY AUTO (Phase 3d-ter): secrets? SQL injection?
    │   └─ Se uno dei check fallisce → retry immediato
    │
    ├─ if score >= threshold:
    │   ├─ ✅ tasks_completed.append(X)
    │   └─ GIT CHECKPOINT: add + commit + push (file esclusivi)
    │
    ├─ if score < threshold AND iteration < max_iterations:
    │   ├─ ❌ Retry IMMEDIATO con feedback
    │
    ├─ if iteration >= max_iterations:
    │   └─ ⚠️ Escalation a Phase 7 (NON accettare automaticamente)
    │
    └─ if ALL tasks done → 🎉 GOAL ACHIEVED
```

## 3a-ter — Actor-Critic (solo dopo 3+ retry)

Distingue tra task difficile e problema strutturale. Max 1 tentativo. Poi escalation.

## 3d — Validazione File Fisici (OBBLIGATORIA Tier 2-4)

File esiste? Non vuoto? No stub/TODO/pass? Sintassi ok? File binario? → ❌ = retry.

## 3d-bis — Execution Reality Check

Per script/test sandboxabili: esegui, usa stderr come feedback del retry. Max 3 tentativi.

## 3d-ter — Security Shield AUTO

Vedi [[Phase 3d-ter - Security Shield AUTO]]. Regex check bloccante per tutti i Tier.

## Adaptive Threshold Tuning (solo prossimo batch)

Se FPR < 60% → prossimo batch con doppia granularità. **Mai cambiare granularità ai task già in volo.**

## Git Commit+Push Policy

- File ESCLUSIVI → commit + push immediato
- File CONDIVISI → solo via Assembly Task post-batch
- DRY CHECK (Tier 3-4) nell'Assembly Task

## Context Window Protection

⚠️ **Critico per Tier 3-4**: dispatch a ondate (warning: oltre 20-25), summary compressi, can_dispatch() preventivo.

## Collegamenti
- [[Fase 2 - Autonomous Scatter]] — Da dove arrivano i risultati
- [[Fase 4 - Self-Learning Loop]] — Impara dai risultati
- [[Fase 6 - Retry Intelligence]] — Retry con convergenza osservata
- [[Fase 7 - Failure Escalation]] — Task non convergenti
- [[Phase 3d-ter - Security Shield AUTO]] — Check sicurezza
- [[Guardrail 11 - Security Shield]] — Guardrail completo
- [[Pitfalls]] — ❌ Context window overflow
