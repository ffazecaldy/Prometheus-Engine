---
tags: [prometheus-engine, fase-7, escalation, failure]
---

# Fase 7 — Failure Escalation Ladder

Scala a 4 livelli quando un task non converge.

```
1. SELF-VERIFY (subagente) — fallito
    ↓
2. RETRY CON FEEDBACK — fallito
    ↓
3. CHANGE STRATEGY — split task, hint architetturale
    ↓
4. 🚨 ESCALATE TO USER
    "Task X non converge dopo N iter.
     Quality: Y/10. Gap: [...]. Come procedo?"
    ↓
5. USER DECIDE — skip / fix manuale / accetta con gap
```

**Regola:** non arrivo al punto 4 senza aver provato 3 strategie diverse.

## Skill da caricare in escalation
- Livello 1: [[skill: systematic-debugging]] — 4-phase root cause
- Livello 2: [[skill: post-mortem]] — 5 Whys + regression test

## Collegamenti
- [[Fase 6 - Retry Intelligence]] — Primo tentativo prima dell'escalation
- [[Fase 10 - Skill Ecosystem]] — Skill per escalation
- [[Fase 8 - Final Report]] — Escalation documentata nel report
