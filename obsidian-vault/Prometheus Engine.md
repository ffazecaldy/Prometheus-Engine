---
tags: [prometheus-engine, hub, mappa]
---

# 🏭 Prometheus Engine — Mappa delle Skill

Benvenuto nella knowledge base del **Prometheus Engine**, il loop agentico autonomo per coding mode.

## Mappa delle Connessioni

```mermaid
graph TD
    Filosofia --> CoreLoop
    CoreLoop --> TierSystem
    TierSystem --> Fase0
    Fase0 --> Fase05[Fase 0.5 - Plan]
    Fase05 --> Fase1[Fase 1 - Decompose]
    Fase1 --> Fase2[Fase 2 - Scatter]
    Fase2 --> Fase3[Fase 3 - Quality Gate]
    Fase3 --> Fase4[Fase 4 - Self Learning]
    Fase4 --> Guardrail
    Fase4 --> PatternCache
    Fase3 --> Fase6[Fase 6 - Retry]
    Fase6 --> Fase7[Fase 7 - Escalation]
    Fase7 --> Fase8[Fase 8 - Report]
    Fase0 --> Fase5[Fase 5 - Scale]
    Fase3 --> Fase10[Fase 10 - Ecosystem]
    Fase10 --> SkillIntegrations
    Filosofia --> Pitfalls
    CoreLoop --> Config
    Config --> UserPrefs
```

## Indice

### 🧠 Fondamenta
- [[4-Band Filter]] — Primo checkpoint: bassa/media/alta/estrema
- [[Filosofia e Core Loop]] — Philosophy, il loop `while goal_not_achieved`
- [[Tier System]] — Come calcolare il tier (1-4) e il Dynamic Subagent Allocation
- [[Configurazione]] — Prerequisiti, environment, hermes config
- [[Preferenze Utente]] — Personalizza lingua, commit policy, decimali, test live
- [[Pitfalls]] — Tutti i fallimenti critici da evitare

### 🔄 Fasi del Loop
- [[Fase 0 - Autonomous Loop Engine]] — Initialize State → Assess → Decide
- [[Fase 0.5 - Plan Integration]] — Clarification interview + Piano strutturato (Tier 3+)
- [[Fase 1 - Massive Decomposition]] — Decomposizione dinamica in task atomici
- [[Fase 2 - Autonomous Scatter]] — Parallel dispatch + streaming
- [[Fase 3 - Streaming Quality Gate]] — Valutazione immediata, retry istantanei
- [[Fase 4 - Self-Learning Loop]] — 3 livelli: memory, pattern cache, skill
- [[Fase 5 - Scale Patterns]] — 4 pattern per sfruttare 100 subagenti
- [[Fase 6 - Retry Intelligence]] — 4 tipi di retry + feedback arricchito
- [[Fase 7 - Failure Escalation]] — Ladder a 4 livelli
- [[Fase 8 - Final Report]] — Report strutturato + self-learning
- [[Fase 10 - Skill Ecosystem]] — Integrazione con altre skill Hermes
- [[Phase 11 - Long Session Management]] — 3 meccanismi per sessioni 2h+
- [[Orchestrator Control]] — Gerarchia 4 livelli per task corposi

### 🛡️ Self-Learning & Guardrail
- [[Guardrail]] — I 10 guardrail non-opzionali
- [[Pattern Cache]] — Token-efficient pattern storage
- [[Lesson Validation]] — Anti-circolarità
- [[Orchestrator Control]] — Gerarchia 4 livelli + B1-B6 anti-bottleneck

### 🧪 Testing & Verifica
- [[E2E Integration Test]] — 35/35 checks su 4 scenari reali
- [[Quality Check]] — Enforcement automatico Phase 9
- `scripts/e2e_test.py` — `python e2e_test.py --verbose`
- `scripts/prometheus_engine.py` — `python prometheus_engine.py` (self-test)
### 📚 Reference Patterns
- [[AI Response Caching]] — Cache SHA256 risposte AI (-92% latenza)
- [[Climatology 3 Levels]] — 3 livelli climatologici (esatto, ±5gg, mese)
- [[Ensemble Confidence Scoring]] — Blended 60/40 objective/subjective
- [[Int-to-Float Precision]] — Da int a 1 decimale per Polymarket betting
- [[External API Integration]] — Multi-fonte con flag e resilienza
- [[Ollama Integration]] — Chiamate Ollama con JSON robusto
- [[Weather API Integration]] — Pattern progetti meteo
- [[Benchmark Harness]] — Benchmark SQLite per skill Hermes
