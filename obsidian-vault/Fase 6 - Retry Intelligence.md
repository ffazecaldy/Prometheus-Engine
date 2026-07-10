---
tags: [prometheus-engine, fase-6, retry]
---

# Fase 6 — Retry Intelligence

## 4 Tipi di Retry

| Tipo | Score | Causa | Strategia |
|------|-------|-------|-----------|
| **SUPERFICIALE** | 5-6 | Quality criteria non letti | Stesso task + feedback |
| **STRUTTURALE** | 3-4 | Approccio sbagliato | Task ridefinito + hint architetturale |
| **GRAVE** | 0-2 | Task mal specificato | Riscrivi da capo, split in micro-task |
| **SILENZIOSO** | N/A | Timeout | Pivota inline: implementa TU |

## Feedback Arricchito

v3: "Mancano 3 edge case specifici: (1) email duplicata → 409, (2) campo vuoto → 400, (3) utente non trovato → 404. Aggiungi test per ognuno."

## Limite Intelligente

- Score migliorato >= 2 punti → continua
- Migliorato < 2 punti → cambia strategia
- Peggiorato → ferma, riparti da zero con task più piccolo

## Collegamenti
- [[Fase 3 - Streaming Quality Gate]] — Dove scattano i retry
- [[Fase 7 - Failure Escalation]] — Quando i retry non bastano
