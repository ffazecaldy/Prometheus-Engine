# 🚀 Prometheus Engine — Autonomous Agentic Loop

> **"I don't follow a workflow. I AM the loop."**

<div align="center">

![Version](https://img.shields.io/badge/version-5.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![For Hermes Agent](https://img.shields.io/badge/for-Hermes%20Agent-orange)
![Subagents](https://img.shields.io/badge/subagents-100%20max-purple)

</div>

---

## 📖 Cos'è Prometheus Engine?

Prometheus Engine è un **framework autonomo per AI coding agent** che trasforma un assistente AI (Hermes Agent) in un sistema auto-regolante che:

- 🧠 **Decide da solo** cosa fare dopo — basato sullo stato corrente, non su un piano fisso
- ⚡ **Esegue in parallelo massivo** — fino a 100 subagenti simultanei (solo quando necessario)
- 🔄 **Valuta e ritenta istantaneamente** — streaming quality gate, nessun batch attesa
- 📚 **Impara e si adatta** — pattern cache, memory compressa, skill promotion
- 🛡️ **Si protegge da sé** — 10 guardrail contro inquinamento, drift, memory overflow

## 🎯 A Chi Serve

| Chi | Perché |
|-----|--------|
| **Utenti Hermes Agent** | Installazione diretta → loop autonomo attivo su ogni prompt di coding |
| **Sviluppatori AI Agent** | Pattern, filosofia e codice da adattare a qualsiasi framework |
| **Team che vogliono agenti autonomi** | Workflow collaudato per sistemi multi-agente self-improving |

## 🚀 Quick Start

### Prerequisiti

```bash
# Hermes Agent — configurazione minima
hermes config set delegation.max_concurrent_children 100
hermes config set delegation.max_spawn_depth 3
hermes config set delegation.max_iterations 100
hermes config set delegation.child_timeout_seconds 300
hermes config set agent.max_turns 120
hermes config set approvals.mode smart
```

### Installazione

```bash
# Con Hermes Agent
hermes skill import https://github.com/ffazecaldy/Prometheus-Engine

# Oppure clona e installa manualmente
git clone https://github.com/ffazecaldy/Prometheus-Engine.git
cp -r Prometheus-Engine/SKILL.md ~/.hermes/skills/
cp -r Prometheus-Engine/references ~/.hermes/skills/
cp -r Prometheus-Engine/scripts ~/.hermes/skills/
```

### Primo utilizzo

Basta chiedere qualcosa di complesso in modalità coding:

```
"Crea un sistema di prenotazione ristorante con API REST + database"
```

Prometheus Engine attiva automaticamente il loop:
1. Rileva il **Tier** (1-4) basato sulla complessità
2. Decompone il goal in task atomici
3. Dispatcha subagenti in parallelo
4. Valuta ogni risultato in streaming
5. Ritenta immediatamente se sotto soglia
6. Salva pattern per la prossima volta

## 🏗️ Struttura del Repository

```
prometheus-engine/
├── SKILL.md                    # La skill principale (il cuore del framework)
├── references/                 # Pattern e best practice
│   ├── orchestrator-control.md # Gerarchia a 4 livelli + 6 regole anti-bottleneck
│   ├── external-api-integration.md
│   ├── ollama-integration.md
│   ├── climatology-3-level.md
│   ├── ai-response-caching.md
│   ├── ensemble-confidence-scoring.md
│   ├── int-to-float-precision.md
│   ├── weather-api-integration.md
│   ├── benchmark-harness-pattern.md
│   ├── config-prerequisites.md
│   └── obsidian-vault-creation.md
├── scripts/                    # Codice Python eseguibile
│   ├── prometheus_engine.py    # Core: detect_band, decompose, quality_check, pattern cache
│   ├── e2e_test.py             # Test end-to-end: 35/35 checks (4 scenari)
│   ├── session_manager.py      # Sessioni lunghe: checkpoint, quality trend, interrupt recovery
│   └── benchmark.py            # Benchmark harness: confronto condizioni
└── obsidian-vault/             # Versione vault Obsidian con graph view
    ├── Prometheus Engine.md    # MOC (Map of Content)
    ├── Fase 0 - ... .md        # Fasi 0-10
    └── ...                     # Pattern, guardrail, configurazione
```

## 🧠 Architettura del Loop

```
while goal_not_achieved:
    state = assess_progress(goal, completed, gaps)
    if state.is_done: break
    tasks = decompose_remaining(state.gaps, state.optimal_scale)
    dispatch_all(tasks)              # scatter: fino a 100 in parallelo
    for each_result in stream():     # gather: processa appena arrivano
        if result.passed: continue
        dispatch_retry(result)       # retry immediato, nessuna attesa
    update_metrics(state)            # self-learning: salva pattern
```

### 4-Band Filter (primo checkpoint)

| Banda | Esempio | Tier | Subagenti | Carica skill? |
|-------|---------|------|-----------|---------------|
| 🟢 **Bassa** | typo, fix bug | 1 | 0 | ❌ (risparmia 8000 token) |
| 🟡 **Media** | endpoint, test | 2 | 1-5 | ✅ |
| 🟠 **Alta** | sistema auth | 3 | 5-30 | ✅ |
| 🔴 **Estrema** | full-stack MVP | 4 | 30-100 | ✅ + orchestrator |

## 🛡️ Self-Learning Guardrail

10 guardrail non-opzionali per prevenire:
- Memory overflow (2200 char budget)
- Circular learning (bias di conferma)
- Skill drift (degradazione silenziosa)
- Skill proliferation (sovrapposizione)
- Project contamination (lezioni cross-progetto)

Dettaglio completo: [Section "Self-Learning Guardrail" in SKILL.md](SKILL.md)

## 📊 Metriche Reali (Benchmark)

| Metrica | Valore |
|---------|--------|
| Punteggio benchmark | **96/100** (24 prompt, 13 categorie) |
| E2E test | **35/35 checks** (100%) |
| Livello equivalente | Senior Developer (5-7yr) |
| Token risparmiati (4-Band Filter) | ~8000 token/task basso |
| Pattern cache | 15+ entry reali su disco |

## 🤝 Come Contribuire

1. **Fork** il repository
2. **Adatta** il template User Preferences al tuo workflow
3. **Aggiungi** pattern al `references/`
4. **Migliora** gli script in `scripts/`
5. **Apri una PR** con descrizione chiara

### Idee per contributi
- Aggiungere un nuovo pattern di decomposizione
- Tradurre la skill in inglese
- Portare i pattern ad altri framework (Claude Code, Codex, Cline)
- Aggiungere benchmark per nuovi scenari

## 📜 Licenza

MIT — vedi [LICENSE](LICENSE)

## 🏆 Credits

Creato da **ffazecaldy** (@Boschi404) con Hermes Agent (Nous Research).

---

<p align="center">
<strong>Prometheus Engine</strong> — Per agenti che migliorano da soli. 🔥
</p>
