# Obsidian Vault Creation — Skill Documentation Pattern

Convertire una skill Hermes in note Obsidian collegate per graph view.

## Quando
Dopo aver sviluppato o aggiornato una skill complessa, se l'utente ha una vault Obsidian e vuole visualizzare le connessioni tra i concetti.

## Procedura

### 1. Analizza la skill
- Leggi SKILL.md con `skill_view(name)`
- Identifica le sezioni principali: ogni Phase/Fase diventa una nota separata
- Identifica i pattern/concetti trasversali (Pitfalls, Guardrail, Config, ecc.)

### 2. Crea la Map of Content (MOC)
- Nota hub con frontmatter YAML + tag + `[[wiki-link]]`
- Include un diagramma Mermaid (graph TD) che mostra le connessioni principali

### 3. Crea le note per ogni sezione
Ogni nota segue questa struttura:
```markdown
---
tags: [skill-name, topic, subtopic]
aliases: [AlternateName]
---

# Titolo Nota

Contenuto essenziale, condensato, puntuale.

## Collegamenti
- [[Nota Collegata 1]] — perché sono collegati
- [[Nota Collegata 2]] — contesto
```

### 4. Collega con wiki-link

| Relazione | Link | Esempio |
|-----------|------|---------|
| Dipendenza | `[[Fase X]]` | Tier System → Fase 1 |
| Pattern afferente | `[[Pattern Name]]` | Climatology 3 Levels → Ensemble Confidence |
| Avvertimento | `[[Pitfalls]]` | ❌ Pitfall specifico |
| Contrappunto | `[[Guardrail]]` | G2: lesson validation |

### 5. Crea note reference
I file `references/*.md` della skill diventano note individuali collegate dalla MOC.

## Convenzioni naming
- Fasi: `Fase N - Nome.md`
- Pattern: `Nome Pattern.md` (Pascal Case)
- Altro: `Nome.md` (Pascal Case)
- Tag: `[skill-name, categoria, sotto-categoria]`

## Collegamenti
- [[Fase 10 - Skill Ecosystem]] — Skill integration patterns
- [[Prometheus Engine]] — MOC example
