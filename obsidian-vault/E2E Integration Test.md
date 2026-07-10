---
tags: [prometheus-engine, test, e2e, integration]
---

# E2E Integration Test

Test end-to-end che simula una sessione di coding completa su 4 scenari reali.

## Scenari Testati

| # | Scenario | Banda | Tier | Checks | Risultato |
|---|----------|-------|------|--------|-----------|
| 1 | Fix rapido — typo in main.py | bassa | 1 | 8/8 | ✅ 100% |
| 2 | Feature media — endpoint CRUD + validazione | media | 2 | 9/9 | ✅ 100% |
| 3 | Sistema auth — JWT + User + servizi + test | alta | 3 | 9/9 | ✅ 100% |
| 4 | Full-stack e-commerce — FastAPI+React+Stripe | estrema | 4 | 9/9 | ✅ 100% |

**Totale: 35/35 checks — 100%**

## Cosa Verifica Ogni Scenario

```
detect_band    → categorizzazione corretta
detect_tier    → tier con familiarity override
decompose      → decomposizione in task atomici
can_dispatch   → context budget enforcement (B6)
quality_check  → file esistenti, no stub, sintassi valida
save_pattern   → pattern_cache.json salvato su disco
load_pattern   → recall del pattern salvato
calibrate      → calibrazione parametri da history
cleanup_cache  → pulizia cache (Guardrail 5)
```

## Esecuzione

```bash
cd scripts/
python e2e_test.py              # esecuzione rapida
python e2e_test.py --verbose    # output dettagliato
python e2e_test.py -v           # shorthand
```

## Risultato Finale

```
RISULTATO FINALE
  Scenari:    4
  Checks:     35/35 (100%)
  Errori:     0
  Durata:     0.1s
  Metriche salvate in pattern_cache.json ✅
```

## Collegamenti
- [[Quality Check]] — Enforcement automatico Phase 9
- [[4-Band Filter]] — Il filtro testato nello scenario 1-4
- [[Prometheus Engine]] — Mappa principale
- `scripts/e2e_test.py` — Script eseguibile
