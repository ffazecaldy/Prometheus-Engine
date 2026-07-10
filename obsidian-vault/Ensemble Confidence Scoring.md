---
tags: [prometheus-engine, pattern, confidence, ensemble]
---

# Ensemble Confidence Scoring

Blended confidence: 60% oggettivo + 40% soggettivo.

## Formula
```
confidence_pct = ensemble_agreement * 0.6 + ai_self_assessment * 0.4
```

## Componenti
- **Ensemble agreement**: quanto i modelli concordano (0-100)
- **Climatology match**: quanto la media modelli si avvicina alla climatologia
- **AI self-assessment**: valutazione di Ollama stessa

## Range Confidenza
| Score | Livello |
|-------|---------|
| ≥ 75% | alto |
| 45-74% | medio |
| < 45% | basso |

## Reasoning
Il confidence_reasoning finale include: `"Accordo tra X% + coerenza climatologica Y%. Score: Z%."`

## Collegamenti
- [[Climatology 3 Levels]] — I dati climatologici alimentano lo score
- [[AI Response Caching]] — Cache riduce latenza senza impattare confidence
- [[Int-to-Float Precision]] — Precisione 1 decimale per betting
