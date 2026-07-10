---
tags: [prometheus-engine, fase-10, ecosystem, skill-integration]
---

# Fase 10 — Skill Ecosystem Integration

Il Prometheus Engine non lavora nel vuoto. Skill complementari vanno caricate durante il loop.

## Tabella Integrazione

| Fase | Skill | Perché |
|------|-------|--------|
| Plan (Tier 3+) | `plan` | Piano strutturato |
| Decompose | `test-driven-development` | Test prima del codice |
| Quality Gate | `verification-strategies` | Quando pytest non disponibile |
| Post-batch | `requesting-code-review` | Pre-commit review |
| Escalation L1 | `systematic-debugging` | Root cause analysis |
| Escalation L2 | `post-mortem` | 5 Whys strutturato |
| Post-deploy | `deploy-release` | Version bump + tag + health check |

## Reference Patterns
- [[AI Response Caching]]
- [[Climatology 3 Levels]]
- [[Ensemble Confidence Scoring]]
- [[Int-to-Float Precision]]
- [[External API Integration]]
- [[Ollama Integration]]
- [[Weather API Integration]]
- [[Benchmark Harness]]

## Collegamenti
- [[Fase 0.5 - Plan Integration]] → skill: plan
- [[Fase 1 - Massive Decomposition]] → skill: tdd
- [[Fase 3 - Streaming Quality Gate]] → skill: verification, code-review
- [[Fase 7 - Failure Escalation]] → skill: debugging, post-mortem
