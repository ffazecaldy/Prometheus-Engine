---
tags: [prometheus-engine, fase-4, self-learning, pattern, knowledge]
---

# Fase 4 — Self-Learning Loop

4 livelli di persistenza, dal più economico al più ricco.

## Livello 1 — Memory Entry Compressa (max 200 char)

Salvata dopo l'ultimo batch della sessione. Solo Livello 1 (LLM Context).

```
PE[goal_type|NomeProgetto|T{N}] FPR=XX% dec=pattern q=X.X iter=N L: lezione
```

## Livello 2 — Pattern Cache File

File JSON in `~/.hermes/pattern_cache.json`. **Zero token cost** (non iniettato in context). Contiene: goal_type, tier, decomposition_pattern, quality_criteria, first_pass_rate, avg_quality, lessons.

## Livello 3 — Skill Dedicata

Se lo stesso goal_type appare 3+ volte con FPR > 75% → crea skill dedicata.

## Livello 4 — Dynamic Knowledge Expansion (Phase 4g)

Vedi [[Phase 4g - Dynamic Knowledge Expansion]] per i dettagli completi.

**Trigger:** 3+ retry su un task. **Split:** 🌍 Globale (tecnologia pura) vs 📁 Locale (convenzioni progetto). **Default:** when in doubt → LOCAL.

## Adaptive Calibration

Adatta i parametri (granularità, soglia, subagenti) basandosi sulla storia persistente del goal_type.

## Token-Efficient Recall

All'inizio di ogni sessione:
1. Memory injection (automatica, PE[...] già in context)
2. Pattern cache check (`pattern_cache.json`)
3. Skill list check (`skills_list`)
4. Dynamic Knowledge check (`local-patterns.md` + `dynamic-patterns.md` filtrato)

## Lesson Hierarchy

| Priorità | Tipo | Salva? |
|----------|------|--------|
| P0 | Structural (cambia strategia futura) | ✅ Sempre |
| P1 | Task-specific (ricorrente) | ✅ Se ricorrente |
| P2 | Context-specific (progetto ricorrente) | ✅ Se progetto ricorrente |
| P3 | One-off (typo, incidente) | ❌ Mai |

## Collegamenti
- [[Guardrail]] — Gli 11 guardrail non-opzionali
- [[Guardrail 11 - Security Shield]] — Security Shield
- [[Pattern Cache]] — Storage efficiente
- [[Lesson Validation]] — Anti-circolarità
- [[Phase 4g - Dynamic Knowledge Expansion]] — Split Local/Global
- [[Fase 8 - Final Report]] — Self-learning log nel report
- [[Pitfalls]] — ❌ Self-learning saltato
