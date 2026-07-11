---
tags: [prometheus-engine, fase-3, quality-gate, streaming, security, execution, git]
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
    │   └─ GIT CHECKPOINT: commit locale sempre, push condizionale
    │
    ├─ if score < threshold AND iteration < max_iterations:
    │   ├─ if retry_count >= 4:
    │   │   └─ ⚠️ ESCALATION IMMEDIATA → Phase 7
    │   └─ else: retry immediato
    │
    ├─ if iteration >= max_iterations:
    │   └─ ⚠️ Escalation a Phase 7 (NON accettare automaticamente)
    │
    └─ if ALL tasks done → 🎉 GOAL ACHIEVED
```

## 3a-bis — Git Commit+Push Policy (condizionale)

**Commit locale: SEMPRE.** Push: condizionale su preferenza utente.

- **`push_mode = "per_task"` (default):** push dopo ogni task superato
- **`push_mode = "batch_end"`:** commit locali per task, push unico a fine batch
- Rilevamento: da prompt utente o clarification interview
- **CI/CD awareness:** se rileva CI, segnala e propone batch_end

## 3d-ter — Security Shield AUTO

Vedi [[Phase 3d-ter - Security Shield AUTO]]. Regex bloccante. Esclude `/tests/` e `/mocks/`. Bypass `# nosec`.

## Adaptive Threshold Tuning (solo prossimo batch)

Se FPR < 60% → prossimo batch con doppia granularità. **Mai cambiare granularità ai task già in volo.**

## Collegamenti
- [[Fase 2 - Autonomous Scatter]] — Da dove arrivano i risultati
- [[Fase 4 - Self-Learning Loop]] — Impara dai risultati
- [[Fase 6 - Retry Intelligence]] — Retry con convergenza osservata
- [[Fase 7 - Failure Escalation]] — Task non convergenti
- [[Phase 3d-ter - Security Shield AUTO]] — Check sicurezza
- [[Guardrail 11 - Security Shield]] — Guardrail completo
- [[Pitfalls]] — ❌ Context window overflow
