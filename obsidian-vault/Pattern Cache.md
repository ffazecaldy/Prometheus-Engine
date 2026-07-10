---
tags: [prometheus-engine, pattern-cache, self-learning]
---

# Pattern Cache

Storage efficiente per pattern ricorrenti.

## Dettaglio
- File JSON in `~/.hermes/pattern_cache.json`
- **Zero token cost** (non iniettato in context)
- Consultabile on-demand quando serve
- Contiene: goal_type, tier, decomposition_pattern, FPR, qualità, lezioni
- Dopo 3 pattern stabili con FPR > 75% → promuovi a skill dedicata

## Regole
- Consultato all'inizio di Phase 1 (decomposizione)
- Se match con FPR > 80% → usa come template, risparmia ~2000 token
- Max 20 entry; se eccede, elimina le 5 più vecchie
- Se goal_type ha 3+ entry con FPR < 60% → elimina tutto quel goal_type

## Collegamenti
- [[Fase 4 - Self-Learning Loop]] — Livello 2 del self-learning
- [[Guardrail]] — G1 (budget), G5 (cleanup)
