---
tags: [prometheus-engine, pattern, caching, AI]
---

# AI Response Caching

Pattern per cache SHA256 delle risposte Ollama.

## Meccanismo
- Chiave: `SHA256(luogo_lower|data|modello)`
- TTL: 6 ore (configurabile)
- Hit → salta chiamata AI (-92% latenza)
- Miss → chiama AI, salva in DB

## Implementazione
- Modello DB: `OllamaResponseCache` (SQLite)
- Cache check in `router.py` prima di chiamare Ollama
- Hit counter per analytics

## Collegamenti
- [[Fase 3 - Streaming Quality Gate]] — Cache riduce latenza
- [[Climatology 3 Levels]] — Pattern simile per climatologia
