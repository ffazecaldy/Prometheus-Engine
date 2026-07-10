---
tags: [prometheus-engine, pattern, climatologia, 3-livelli]
---

# Climatology 3 Levels

Pattern per climatologia a 3 livelli di profondità.

## I 3 Livelli

| Livello | Campioni | Descrizione |
|---------|----------|-------------|
| Giorno esatto | ~10 | 10 anni × stesso giorno |
| Finestra ±5gg | ~100 | 10 anni × 11 giorni |
| Mese intero | ~310 | 10 anni × ~31 giorni |

## Vantaggio
Da 10 a **310 campioni** → statistiche 30× più robuste. La confidenza AI si basa su dati molto più rappresentativi.

## Singola API Call
Open-Meteo Archive accetta range date → una sola chiamata per tutti e 3 i livelli.

## Collegamenti
- [[Ensemble Confidence Scoring]] — La confidenza usa questi dati
- [[Fase 4 - Self-Learning Loop]] — Pattern salvato dopo implementazione
