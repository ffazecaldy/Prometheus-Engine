---
tags: [prometheus-engine, guardrail, self-learning]
---

# Guardrail — I 10 Non-Opzionali

Il self-learning autonomo **senza guardrail è pericoloso**. Questi sono obbligatori.

## G1 — Memory Budget Cap
Max 2200 char totali. Max 8-10 entry PE[...]. Nuove sostituiscono vecchie.

## G2 — Lesson Validation (anti-circolarità)
Una lezione è valida SOLO SE confermata da test fallito + fix, o pitfall tecnico. Niente "ho provato X e ha funzionato".

## G3 — Skill Mutation Protection
Permesso patch pitfalls/references. Vietato modificare Philosophy/Tier/Criteri/Guardrail senza conferma utente.

## G4 — Skill Proliferation Cap
Max 5 skill pattern-*. Max 1 skill creata per sessione. Se 2 skill >70% simili → consolida.

## G5 — Pattern Cache Cleanup
Ogni 10 batch: se >20 entry, elimina le 5 più vecchie. Se >50, emergenza: tieni solo top 10 con FPR>70%.

## G6 — Project Isolation
Lezioni tecniche globali = valide ovunque. Lezioni architetturali/UI = progetto-specifiche, marcate con prefisso.

## G7 — Human Checkpoint
Nessuna skill creata/modificata/cancellata senza consenso umano. Patch permesse ma notifica sempre.

## G8 — Session Memory Flush Cap
Max 3 memory entry PE[...] per sessione. Max 1 skill patch. Max 1 pattern_cache update.

## G9 — Drift Detection
Ogni 5 sessioni: se FPR cala >10% → STOP apprendimento, segnala drift, proponi reset lezioni.

## G10 — Transparency Log
Ogni operazione di self-learning tracciata nel final report: quante entry, quali patch, quali lezioni validate/scartate.

## Collegamenti
- [[Fase 4 - Self-Learning Loop]] — Il loop che i guardrail proteggono
- [[Lesson Validation]] — G2 in dettaglio
- [[Pattern Cache]] — G1, G5 coinvolti
- [[Fase 8 - Final Report]] — G10: transparency log
