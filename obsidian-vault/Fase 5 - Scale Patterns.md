---
tags: [prometheus-engine, fase-5, scale, pattern]
---

# Fase 5 — Scale Patterns

4 pattern per sfruttare veramente 100 subagenti.

## Pattern A — Multi-Implementazione + Voting
Task 1-5: 5 varianti dello stesso modulo (approccio diverso)
Task 6: Valutatore sceglie la migliore
Task 7-N: task normali

## Pattern B — Ricerca + Implementazione + Test
Task 1-10: Ricerca esplorativa (10 angolazioni)
Task 11-60: Implementazione (50 task atomici)
Task 61-80: Test paralleli (20 suite)
Task 81-90: Documentazione
Task 91-100: Review incrociata

## Pattern C — Full System Build
Task 1-5: Setup (DB, auth, config, CI, deploy)
Task 6-20: Modelli e DB layer
Task 21-50: API routes
Task 51-70: Frontend
Task 71-85: Test
Task 86-95: Documentazione
Task 96-100: Integration review + deploy

## Pattern D — Data Pipeline Massiva
Task 1-20: Fetch da 20 fonti
Task 21-40: Trasforma/normalizza
Task 41-60: Analizza/metriche
Task 61-80: Merge e correla
Task 81-90: Report/visualizzazioni
Task 91-100: Review

## Collegamenti
- [[Tier System]] — Pattern attivati in base al Tier
- [[Fase 2 - Autonomous Scatter]] — Dispatch dei pattern
- [[Fase 1 - Massive Decomposition]] — Decomposizione che alimenta i pattern
