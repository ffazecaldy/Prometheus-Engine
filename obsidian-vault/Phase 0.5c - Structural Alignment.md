---
tags: [prometheus-engine, fase-05c, scaffolding, architecture]
---

# Phase 0.5c — Structural Alignment (Scaffolding Adattivo)

Prima di assegnare path ai file, l'agente DEVE allinearsi alla struttura esistente o crearne una proporzionata al Tier.

## Regola 1: Scan First

```
├─ search_files per rilevare convenzioni già esistenti nel repo
│   └─ Es: se esiste app/routers/ → nuovo codice API va lì
│   └─ Es: se esiste src/components/ → nuovo frontend va lì
├─ MAI creare una cartella parallela se ne esiste già una con lo stesso scopo
└─ Se il progetto è nuovo (greenfield, zero convenzioni) → applica Regola 2
```

## Regola 2: Architettura Proporzionata al Tier

**Tier 1-2 (Bassa/Media):** Struttura piatta o minimale.
- `main.py`, `utils.py`, `test_main.py`
- NIENTE layer di astrazione inutili (no Repository Pattern per uno script)
- NIENTE cartelle vuote o pre-create "per il futuro"

**Tier 3-4 (Alta/Estrema):** Separazione modulare dei livelli.
- `models/` → persistenza e schema dati
- `services/` → business logic
- `api/` o `routers/` → esposizione HTTP
- `tests/` → test suite
- `config/` → configurazione centralizzata

## Regola 3: Greenfield Fallback

- Progetto nuovo, zero convenzioni, Tier 1-2: crea `main.py` + `tests/` (basta)
- Progetto nuovo, zero convenzioni, Tier 3-4: crea struttura modulare sopra

## Collegamenti

- [[Fase 0.5 - Plan Integration]] — Dove si inserisce nel flusso
- [[Tier System]] — Come viene determinato il Tier
- [[Fase 1 - Massive Decomposition]] — La decomposizione usa i path allineati
