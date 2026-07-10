---
tags: [prometheus-engine, fase-4g, knowledge, anti-overfitting]
---

# Phase 4g — Dynamic Knowledge Expansion (Local/Global Split)

**Trigger:** 3+ retry su un task. Cattura la regola risolutiva per evitare di ripetere lo stesso errore.

## ⚠️ Regola Fondante (Anti-Overfitting)

Non tutta la conoscenza è globale. Salvare pattern specifici di un progetto come globali = **Context Contamination** = il sistema diventa inutilizzabile su progetti diversi.

## Split 🌍 Globale vs 📁 Locale

### 🌍 SCOPE GLOBALE — Tecnologia pura

**Criterio:** la lezione vale per QUALSIASI progetto che usa quella tecnologia.

- `~/.hermes/references/dynamic-patterns.md`
- Esempi:
  - "React 19 — use() sostituisce useContext per Promise"
  - "Stripe API v2024 — il parametro 'amount' ora è in centesimi"
  - "Python 3.12 — typing.TypeAlias sostituisce TypeAlias da typing_extensions"

### 📁 SCOPE LOCALE — Architettura di progetto

**Criterio:** la lezione vale SOLO per questo specifico progetto.

- `./.hermes/local-patterns.md` (crealo se non esiste)
- Esempi:
  - "In questo progetto, le route FastAPI vanno in routers/ non api/"
  - "Usare sempre il custom wrapper get_db_session(), mai Session() diretta"
  - "I validatori Pydantic vanno in app/validators.py, non nei models"

### ⚠️ DEFAULT

**When in doubt → LOCAL.** Un pattern locale iniettato in un altro progetto è rumore innocuo. Un pattern globale iniettato dove non serve è danno.

## Caricamento nei Task Futuri (Tier 2-4)

```
├─ Leggi SEMPRE ./.hermes/local-patterns.md (se esiste nel progetto corrente)
├─ Leggi ~/.hermes/references/dynamic-patterns.md SOLO per le tecnologie citate nel goal
│   └─ Esempio: goal contiene "React" → carica solo le entry React
└─ Inietta le regole rilevanti come extra_criteria nei context dei subagenti
```

## Guardrail di Proliferazione

- File GLOBALE: max 50 entry, archivio automatico delle più vecchie con <2 occorrenze
- File LOCALE: nessun limite (cresce col progetto, muore col progetto)
- Formato `[Auto]` — autonomo, non richiede checkpoint umano (Guardrail 7)

## Collegamenti

- [[Fase 4 - Self-Learning Loop]] — Dove si inserisce (Livello 4)
- [[Guardrail]] — G6 (Project Isolation) e G7 (Human Checkpoint)
- [[Fase 1 - Massive Decomposition]] — Dove vengono iniettate le regole
- [[Guardrail 11 - Security Shield]] — Check complementare
