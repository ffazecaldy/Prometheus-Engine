---
tags: [prometheus-engine, guardrail-11, security, owasp]
---

# Guardrail 11 — Security Shield

**No vulnerabilities by design.** Opera su due livelli: AUTO (bloccante) e REVIEW (Actor-Critic).

## LIVELLO AUTO — Regex (Phase 3d-ter, TUTTI i Tier)

Eseguito dopo validazione fisica ed execution check, prima del quality gate. Se fallisce → ❌ retry immediato.

| # | Regola | Verifica |
|---|--------|----------|
| 1 | Zero Hardcoded Secrets | Regex: `api_key = '...'` senza `getenv` |
| 2 | No Raw SQL Injection | Regex: f-string/format/concat con SQL |
| 3 | Placeholder Warning | Regex: `API_KEY = '' # TODO` → ⚠️ log |

## LIVELLO REVIEW — Actor-Critic (Phase 3a-ter, SOLO Tier 3-4)

Applicato quando un task ha 3+ retry o è di tipo API/auth/security. **Non bloccante automatico** — richiede comprensione semantica.

| # | Regola | Verifica |
|---|--------|----------|
| 4 | Input Validation | Route API hanno schema validazione (Pydantic/Zod)? |
| 5 | Error Info Leakage | Stack trace mai esposto all'utente? Try/except con messaggi generici? |
| 6 | Safe Dependencies | Versioni pinnate (`==`, non `>=`)? Package da fonti note? |

## Collegamenti

- [[Guardrail]] — Tutti gli 11 guardrail
- [[Phase 3d-ter - Security Shield AUTO]] — Implementazione regex (LIVELLO AUTO)
- [[Fase 3 - Streaming Quality Gate]] — Dove si inserisce nella pipeline
- [[Fase 6 - Retry Intelligence]] — Actor-Critic (LIVELLO REVIEW)
- [[Quality Check]] — Modulo quality_check.py con Check 5 security
