---
tags: [prometheus-engine, pitfalls, errori]
---

# Pitfalls — Errori Critici

## ❌ Il loop non è veramente autonomo
Valuta stato → agisci → ripeti. Non "pianifica → pianifica ancora → agisci".

## ❌ Streaming gather dimenticato
I retry devono partire APPENA arriva un risultato sotto soglia.

## ❌ Orchestrator bottleneck — 6 Trappole Strutturali
Risolte con regole B1-B6 (vedi [[Orchestrator Control]]):
1. B1: Serializzazione → mini-batch da 5
2. B2: Costo token → depth auto-limit
3. B3: Perdita contesto → snapshot <200 token
4. B4: Retry amplification → degradazione inline
5. B5: Timeout conflict → allineati 60-120-240-300
6. B6: Context overflow → can_dispatch() preventivo

## ❌ Subagenti su codebase familiare
Se conosci il codebase, 0 subagenti. L'overhead di dispatch non si ripaga.

## ❌ Context window overflow
100 subagenti × 2000 token = 200K token. Dispatcha a ondate di 20-25.

## ❌ Python .pyc cache
Su Windows, `.pyc` può essere più recente del `.py`. Elimina `__pycache__` o usa `python -B`.

## ❌ Server zombie sulla porta
Il vecchio processo resta in ascolto. Il nuovo crasha con `[Errno 10048]`.
**Procedura:** netstat → taskkill → verifica → avvia → verifica codice fresco.

## ❌ Saltare clarification interview (Tier 3+)
2 minuti di domande risparmiano 20 minuti di retry.

## ❌ Self-learning senza guardrail
Memory overflow, circular learning, skill drift, project contamination.

## ❌ Modelli cloud Ollama richiedono abbonamento
`:cloud` tag richiede `ollama login` e talvolta pagamento. Verifica con curl prima.

## ❌ FastAPI route ordering
Route statiche PRIMA di `/{param}`.

## Collegamenti
- [[Filosofia e Core Loop]] — ❌ Loop non autonomo
- [[Fase 3 - Streaming Quality Gate]] — ❌ Streaming gather
- [[Fase 0.5 - Plan Integration]] — ❌ Saltare clarification
- [[Guardrail]] — ❌ Self-learning senza guardrail
- [[Configurazione]] — ❌ Ollama cloud
