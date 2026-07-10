---
tags: [prometheus-engine, fase-1d-bis, clean-code, quality]
---

# Phase 1d-bis — Clean Code Standards

Criteri di qualità del codice, applicati per Tier. **Mai su Tier 1** (overkill).

## 1. Type Hints & Docstrings (Tier 2-4, obbligatorio)

- Ogni funzione deve avere type hints espliciti (parametri e ritorno)
- Ogni funzione pubblica deve avere una docstring concisa
- Formato: `[Cosa fa]. Input: [parametri]. Output: [ritorno]. Raises: [eccezioni].`
- **Verificabile automaticamente** via fase di validazione

## 2. Single Responsibility — SRP (Tier 3-4, via Actor-Critic)

- Una funzione/classe fa UNA cosa sola
- Se una route API fa DB query + business logic + email → ❌ BOCCIATO
- **Applicato SOLO dopo 3+ retry** (non per ogni task — costoso)
- Verificato dall'[[Fase 6 - Retry Intelligence#3a-ter|Actor-Critic]], non da regex

## 3. DRY — Don't Repeat Yourself (Tier 3-4, via Assembly Task)

- Se due subagenti producono codice duplicato, l'Assembly Task lo estrae
- Destinazione: modulo condiviso (`utils/` o `config/`)
- **Applicato POST-BATCH**, non durante il dispatch individuale
- Verificato dall'Assembly Task (Phase 3a-bis punto 6)

## Collegamenti

- [[Fase 1 - Massive Decomposition]] — Dove i criteri vengono iniettati
- [[Fase 3 - Streaming Quality Gate]] — Actor-Critic + Assembly Task
- [[Tier System]] — Determina quali criteri applicare
- [[Phase 3d-ter - Security Shield AUTO]] — Check complementare di sicurezza
