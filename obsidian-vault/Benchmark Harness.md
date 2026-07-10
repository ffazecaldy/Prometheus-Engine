---
tags: [prometheus-engine, pattern, benchmark, harness]
---

# Benchmark Harness

Costruire benchmark harness per skill Hermes.

## Componenti
- **SQLite metrics**: persistenza metriche performance
- **verify_cmd ground truth**: comando di verifica come oracle
- **Parser isolato**: estrazione strutturata dati
- **Confronto multi-condizione**: baseline / v1 / v2

## Output
Metriche confrontabili: MAE, RMSE, bias, accuracy per confidence level.

## Collegamenti
- [[Ensemble Confidence Scoring]] — Metriche per confidence
- [[Climatology 3 Levels]] — Benchmark climatologia
