---
name: prometheus-engine
description: "Always-on autonomous agentic loop: prompt enhancement → deep research → massive scatter-gather (up to 100 subagents) → streaming quality gate (immediate retry on arrival) → self-learning iteration. Autonomous in execution, collaborative in mutation. Auto-activates on EVERY programming-mode prompt."
version: 5.2.0
author: Prometheus Engine Community
repository: https://github.com/ffazecaldy/Prometheus-Engine
tags: [prometheus, engine, auto, workflow, multi-agent, quality, research, iteration, scatter-gather, streaming-gather, self-learning, autonomous-loop, meta-scaling, quick-start]
---

# Prometheus Engine — Autonomous Loop Engine

## Philosophy

**I don't follow a workflow. I AM the loop. Autonomous in execution, collaborative in mutation.**

This skill transforms me into an autonomous agentic system that:

1. **Decides what to do next** — based on current state, not a fixed plan
2. **Executes massively in parallel** — up to 100 subagents per batch, BUT ONLY WHEN NEEDED
3. **Evaluates and retries instantly** — streaming gather, no batching delays
4. **Learns and adapts** — saves patterns, improves next iteration
5. **Keeps going until done** — autonomous in execution, collaborative in mutation

---

### ⚖️ REGOLA DI PRECEDENZA — Conflitti tra policy

Se due sezioni descrivono policy alternative per lo stesso momento del flusso, **vince la più restrittiva** (sicurezza > autonomia). Ordine di precedenza:

1. ⚖️ **Regola di Precedenza** (questa sezione) — sempre attiva
2. 🛡️ **Guardrail (Phase 4f)** — proteggono il sistema da se stesso
3. 🪜 **Escalation Ladder (Phase 7)** — l'utente decide su gap sotto soglia
4. 🧠 **Context Protection (Phase 3e)** — previene overflow/saturazione
5. ✨ **Quality Gate (Phase 3a)** — valuta e ritenta
6. 📡 **Scatter (Phase 2a)** — dispatch parallelo

**Esempio concreto:** se Phase 3a dice "accetta task sotto soglia" ma Phase 7 dice "escala all'utente" → vince Phase 7. Se Phase 2a dice "dispatcha 50 subagenti in streaming" ma Phase 3e dice "max 20-25 in-flight" → vince Phase 3e.

### ⚠️ REGOLA FONDAMENTALE — Dynamic Subagent Allocation

**100 subagenti è il tetto massimo, NON il default.** Il numero di subagenti dispatchati è determinato dinamicamente dal Tier system. Mai usare più subagenti del necessario.

```
DYNAMIC ALLOCATION (OBBLIGATORIO):
  Tier 1 → 0 subagenti (eseguo io, direttamente, nessun overhead)
  Tier 2 → 1-5 subagenti (batch piccolo, fast path)
  Tier 3 → 5-30 subagenti (solo se il task lo richiede davvero)
  Tier 4 → 30-100 subagenti (solo per sistemi full-stack complessi)

PRIMA di dispatchare, chiediti SEMPRE:
  "Questo task ha davvero bisogno di N subagenti?"
  "Posso farlo io direttamente in meno tempo di quello che serve per dispatchare?"

REGOLA DEL RISPARMIO:
  Se un task può essere fatto da me direttamente in <30 secondi → fatelo io, 0 subagenti
  Se un task richiede 1-2 file → 1 subagente, non 5
  Se un task richiede 3-5 file correlati → 2-3 subagenti, non 10
  Solo sistemi multi-componente (5+ entità, 3+ API, multi-layer) giustificano 10+ subagenti
```

#### 🧠 Fattore Familiarità — Override del Tier

Il Tier system assume codebase **sconosciuto**. Se invece **conosci già il codebase** (esplorato in sessioni precedenti, hai letto i file chiave, conosci la struttura), puoi applicare un override:

| Conoscenza codebase | Adeguamento subagenti |
|---|---|
| Mai visto (prima sessione sul progetto) | Tabella standard |
| Esplorato in sessione precedente | -50% subagenti |
| Conosci a memoria (letto >5 file) | -80% subagenti (o 0) |
| Tu stesso hai scritto il modulo | 0 subagenti, esecuzione diretta |

**Esempio reale:** 10 file da modificare, 6 API esterne → Tier 3 (5-30 subagenti). MA codebase già esplorato in 3+ sessioni precedenti → Familiarità alta → 0 subagenti, esecuzione diretta. Risultato: FPR 100%, qualità 9/10, 8 minuti totali.

**Regola pratica:** se hai già letto i 5 file principali del progetto, sei in Familiarità Media. Se hai già scritto file in quel progetto, sei in Familiarità Alta. Riduci i subagenti proporzionalmente. L'overhead di dispatch non si ripaga su codebase che già conosci.

**Il costo di 100 subagenti paralleli è 100× il costo di un singolo turno API.** Disperderli su task semplici è uno spreco di token e denaro. Usa il minimo indispensabile.

**The core loop (always running):**

```
while goal_not_achieved:
    state = assess_progress(goal, completed, gaps)
    if state.is_done: break
    tasks = decompose_remaining(state.gaps, state.optimal_scale)
    dispatch_all(tasks)              # scatter: up to 100 in parallel
    for each_result in stream():     # gather: process as they arrive
        if result.passed: continue
        dispatch_retry(result)       # immediate retry, no waiting
    update_metrics(state)            # learn: save patterns
```

---

## 🚀 Quick Start — Esempio Reale del Loop

Vediamo il loop in azione su un goal concreto:

```
GOAL: "Crea un sistema di prenotazione ristorante con API REST + database"

1. STATE INIT ──────────────────────────────────────────────
   tier: 3 (5-20 files, 5-30 subagenti)
   soglia: 7/10
   subagenti: 100 disponibili

2. DECOMPOSE (Phase 1) ────────────────────────────────────
   50 task atomici, 1 file ciascuno:
   ├── models/ (restaurant, reservation, menu, user, review)
   ├── routes/ (CRUD per ogni entità + auth + search)
   ├── services/ (disponibilità, notifiche, pagamenti)
   ├── tests/ (test per ogni endpoint)
   └── docs/ (README, API docs, setup guide)

3. SCATTER (Phase 2) ──────────────────────────────────────
   Dispatch 50 subagenti in parallelo.
   Ogni subagente riceve: task specifico + quality criteria + soglia 7/10

4. STREAMING GATHER (Phase 3) ──────────────────────────────
   ┌─ Risultato 1: models/restaurant.py → score 8/10 ✅
   ├─ Risultato 2: routes/reservations.py → score 4/10 ❌
   │   └─ RETRY IMMEDIATO: "Manca validazione date, conflitto orari"
   ├─ Risultato 3: models/user.py → score 9/10 ✅
   ├─ Risultato 4: services/notifications.py → score 5/10 ❌
   │   └─ RETRY IMMEDIATO: "Manca fallback email, template notifica"
   ├─ ... 46 altri risultati in streaming ...
   └─ Retry 2 converge → score 8/10 ✅

5. CONVERGENZA (Phase 4) ──────────────────────────────────
   Iterazione 1: 50 task → 42 pass (84%), 8 fail
   Iterazione 2: 8 retry → 6 pass, 2 fail (migliorati ma sotto)
   Iterazione 3: 2 retry con hint architetturale → 2 pass (100%)
   → 🎉 GOAL ACHIEVED in 3 iterazioni

6. SELF-LEARNING (Phase 4) ────────────────────────────────
   Pattern salvato: "decomposizione per_file per sistemi CRUD"
   First-pass rate: 84% (eccellente)
   Lesson: "Task di servizi (notifiche/pagamenti) hanno FPR più basso"
   → Prossima volta: quality criteria più specifici per servizi

7. REPORT (Phase 8) ────────────────────────────────────────
   Subagenti usati: 50 / 100 disponibili
   First-pass rate: 84%
   Convergenza: 3 iterazioni
   Qualità media: 8.6/10
   Durata: ~5 min
```

Questo è il loop. Gira da solo. Non serve intervento umano tra uno step e l'altro.

---

## Prerequisites & Configuration (CRITICO)

Questa skill presuppone 100 subagenti paralleli. **Senza i settaggi config.yaml corretti, il default è 3 subagenti e tutto il sistema è castrato.**

Verifica questi settaggi prima di attivare il loop:

```bash
hermes config set delegation.max_concurrent_children 100  # default 3 → 100 (tetto max, dinamico)
hermes config set delegation.max_spawn_depth 3             # default 1 → 3 (orchestrator→leaf→micro-worker)
hermes config set delegation.max_iterations 100            # default 50 → 100 (iterazioni per subagente)
hermes config set delegation.child_timeout_seconds 300     # default 0 → 300 (B5: allineato con cascade 4 livelli)
hermes config set delegation.subagent_auto_approve true    # default false → true (subagenti possono git push)
hermes config set agent.max_turns 120                      # default 60 → 120 (loop complessi Tier 4)
hermes config set approvals.mode smart                     # default manual → smart (auto-approva low-risk)
hermes config set code_execution.max_tool_calls 100        # default 50 → 100 (pipeline dati complesse)
hermes config set compression.protect_first_n 5            # default 3 → 5 (proteggi goal + piano)
```

Verifica che siano attivi:
```bash
grep -E "max_concurrent_children|max_spawn_depth|max_turns|approvals" ~/.hermes/config.yaml
```

**Importante:** le modifiche al config richiedono una **nuova sessione** (`/reset` o riavvia Hermes) per avere effetto. Nella sessione attiva i vecchi valori restano attivi.

Vedi `references/config-prerequisites.md` per dettagli completi su ogni impostazione e toolset richiesti.

---

## Trigger Conditions

Questa skill si attiva quando l'utente dice qualcosa che indica siamo in **modalità programmazione/progetto**, ad esempio:
- "programma", "sviluppa", "crea", "implementa", "build", "code", "project"
- "prometheus", "modalità prometheus", "prometheus engine"
- "modalità programmazione", "coding mode"
- Richieste che coinvolgono codice, architettura, sistemi, API, database
- Task multi-file o multi-componente
- Qualsiasi richiesta che richiederebbe 3+ step

Quando non attiva:
- Domande semplici, chat informale, lettura file, domande su Hermes stesso

## 🎯 4-Band Filter — Primo Checkpoint (PRIMA di tutto)

**PRIMA di caricare il resto della skill**, categorizza la richiesta in 4 bande.
Questo determina QUANTO della skill attivare.

```
BANDA BASSA → Tier 1, NON caricare SKILL.md completo, esecuzione diretta
BANDA MEDIA → Tier 2, carica skill, max 1-5 subagenti
BANDA ALTA → Tier 3, carica skill completa, 5-30 subagenti
BANDA ESTREMA → Tier 4, carica tutto, 30-100 subagenti, orchestrator
```

| Banda | Esempi | Tier | Carica skill? | Subagenti | Loop? |
|-------|--------|------|---------------|-----------|-------|
| **Bassa** | typo, fix bug, cambia colore, rinomina | 1 | ❌ No (risparmia 30KB) | 0 | No, diretto |
| **Media** | aggiungi endpoint, crea funzione, test, refactoring | 2 | ✅ Sì | 1-5 | 1 iterazione |
| **Alta** | sistema, modulo auth, API completa, multi-file feature | 3 | ✅ Sì | 5-30 | ∞ converge |
| **Estrema** | full-stack, e-commerce, MVP da zero, 50+ file | 4 | ✅ Sì | 30-100 | ∞ + orchestrator |

### Implementazione

Lo script `scripts/prometheus_engine.py` contiene la funzione `detect_band(prompt)` che classifica automaticamente:

```python
from prometheus_engine import detect_band, band_to_config

band = detect_band("correggi typo nel file main.py")  # → "bassa"
config = band_to_config(band)
# config = {"tier": 1, "load_skill": False, "subagents": 0, ...}

band = detect_band("crea piattaforma e-commerce full-stack")  # → "estrema"
config = band_to_config(band)
# config = {"tier": 4, "load_skill": True, "subagents": 30, ...}
```

### Regola di Risparmio Token

```
SE banda == "bassa":
  └─ NON caricare SKILL.md (30KB = ~8000 token risparmiati)
  └─ Esegui direttamente: leggi file, modifica, commit, push
  └─ Nessun loop, nessun subagente, nessun piano

SE banda == "media":
  └─ Carica SKILL.md
  └─ Fast path: decompose → dispatch 1-5 → gather → done
  └─ Max 1 retry, niente self-learning

SE banda == "alta" o "estrema":
  └─ Carica SKILL.md completo
  └─ Loop completo con tutte le fasi
  └─ Self-learning attivo
```

## 📋 User Preferences — Configurable Template

**Personalizza questa sezione per adattare Prometheus Engine al TUO workflow.**
Copia/modifica le voci che ti servono. Le preferenze attive vengono iniettate nel loop automaticamente.

### Esempio di configurazione (da personalizzare):

```yaml
# Lingua output
language: "italiano"          # o "english", "español", etc.

# Git workflow
auto_commit: true             # commit dopo ogni task passato?
auto_push: true               # push immediato dopo commit?

# Testing
live_test_backend: true       # curl/chiamata HTTP dopo ogni backend change?
test_command: "pytest -q"     # comando test suite

# Preferences specifiche del progetto
# (esempi - rimuovi o modifica secondo necessità)
temperature_decimals: 1       # decimali per temperature (betting)
quick_cities_offset: 1        # giorni avanti per data predefinita
static_header: true           # header UI statico
climatology_context: true     # storico climatologico (mediana, percentili, trend, anomalia)

# Feedback
self_feedback: true           # autovalutazione 0-100% alla fine del task
```

### Come usarlo

1. Copia questo template nel tuo config di progetto (es. `prometheus-config.yaml` o nella sezione memory del tuo profilo Hermes)
2. Modifica i valori secondo le tue preferenze
3. Il loop di Prometheus Engine legge automaticamente queste preferenze e adatta il comportamento

> **Nota per contributor:** Se forkhi questa skill, sostituisci questa sezione con le tue preferenze. La skill è progettata per essere adattabile a qualsiasi stack e workflow.

---

## Tier System — Adaptive Depth (auto-calibrated)

Non scelgo più il tier a priori. Lo calcolo dinamicamente in base alla complessità percepita e alla risposta iniziale dei subagenti.

| Fattore | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|--------|--------|--------|--------|
| **Files coinvolti** | 0-1 | 2-5 | 5-20 | 20-100+ |
| **Subagenti batch** | 0 | 1-5 | 5-30 | 10-100 |
| **Soglia qualità** | — | 6/10 | 7/10 | 8/10 |
| **Loop autonomo** | No | Sì (1 iter) | Sì (∞, converge) | Sì (∞, converge) |
| **Auto-apprendimento** | No | Pattern base | Pattern + metriche | Pattern + metriche + skill |
| **Fast path** | Diretto | Compresso 2 step | Completo | Completo |

**Regola:** Se il primo batch ha first-pass rate > 80%, il tier era giusto. Se < 60%, scala di un livello (più subagenti, task più piccoli).

### Tier Detection — Criteri Operativi Numerici

Non indovinare il tier. Calcolalo con questa formula:

Implementazione reale: `scripts/prometheus_engine.py` → `detect_tier()`

```python
from prometheus_engine import detect_tier

# Senza repo scan (stima dal prompt)
tier = detect_tier("crea sistema prenotazione con 4 entità", familiarity="nessuna")  # → 3

# Con repo scan + familiarità alta (override)
tier = detect_tier("crea sistema prenotazione", repo_scan={"import_count": 5, "external_integrations": 2}, familiarity="alta")  # → 1
```

Formula interna (in `prometheus_engine.py`):
```python
complexity = (files_likely * 1.0) + (existing_deps * 0.5) + (has_external_apis * 2.0)
# Tier base: ≤2→T1, ≤10→T2, ≤40→T3, >40→T4
# Familiarity override: nessuna→0, bassa→0, media→-1, alta→-2 (min Tier 1)
```

**Esempi concreti:**
- "Aggiungi validazione email al form di login" → 1 file, 0 dipendenze nuove → **Tier 1**
- "Crea endpoint /api/users con CRUD + 3 test" → 2 file (route + test), 1 dipendenza (model) → **Tier 2**
- "Sistema prenotazione ristorante con 4 entità + auth + notifiche" → 15+ file, 3 entità, 2 API esterne → **Tier 3**
- "Piattaforma e-commerce full-stack con pagamenti + admin + frontend" → 50+ file, multi-layer → **Tier 4**

### Fast Path — Tier 1 e 2

Per task semplici, il loop si comprime in 2 passi invece di 10:

```
TIER 1 (0-1 file):
  └─ Phase 0: risposta diretta, nessun loop

TIER 2 (1-5 subagenti):
  ├─ Phase 0: decomponi in 1-5 task
  ├─ Phase 2: dispatch 1-5 subagenti
  └─ Phase 3: streaming gather + al max 1 retry
      └─ Se tutto passa → final report (compresso: 3 righe)
      └─ Se 1 fallisce → retry + report
```

Niente self-learning, niente escalation ladder, niente pattern capture. Solo execute → verify → done.

---

## Phase 0 — Autonomous Loop Engine

Questa è la fase che sostituisce tutte le altre. Non seguo fasi in ordine — eseguo il loop finché il goal non è raggiunto.

### 0a — Initialize State

All'inizio di ogni richiesta, inizializzo lo stato:

```python
STATE = {
    "goal": "prompt_enhanced",
    "tier": auto_detect(),
    "quality_threshold": tier_to_threshold(tier),
    "subagents_available": 100,      # max_concurrent_children
    "subagents_used": 0,
    "tasks_completed": [],
    "tasks_failed": [],
    "tasks_in_flight": [],
    "iteration": 0,
    "max_iterations": auto_calc(tier),
    "first_pass_rate": None,
    "avg_quality_score": None,
    "self_lessons": [],              # pattern salvati da iterazioni precedenti
    "start_time": now(),
}
```

### 0b — State Assessment (dopo ogni evento)

Ogni volta che ricevo un risultato (o all'inizio), valuto lo stato:

```
ASSESS:
1. Cosa è stato completato? (tasks_completed)
2. Cosa è fallito? (tasks_failed + gaps)
3. Ci sono task in-flight? (tasks_in_flight)
4. Il goal è raggiungibile? (gaps vs risorse rimanenti)
5. Devo cambiare strategia? (first_pass_rate < 60% → più granularità)
6. Ho già pattern salvati per questo tipo di task?
```

### 0c — Decisione Autonoma

Basandomi sullo stato, decido COSA fare ORA:

```
if tasks_in_flight:
    └─ aspetto risultati (streaming)
elif tasks_failed and iteration < max_iterations:
    └─ retry con feedback arricchito
elif tasks_failed and iteration >= max_iterations:
    └─ escalo all'utente (con qualità documentata)
elif not tasks_completed:
    └─ decomponi goal in task atomici → dispatch
elif tasks_completed and avg_quality >= threshold:
    └─ COMPLETO → final report + self-learning
elif tasks_completed and avg_quality < threshold:
    └─ quality improvement loop (affina而非 rifa)
```

**NON aspetto.** Ogni decisione è immediata. Il loop gira senza che l'utente debba intervenire.

---

## Phase 0.5 — Plan Integration (Tier 3+ only)

Per Tier 1 e 2, il loop va dritto alla decomposizione (Phase 1). Per **Tier 3 e 4**, una fase di pianificazione strutturata PRIMA dello scatter riduce i retry del 30-40%.

### 0.5a — Clarification Interview (PRIMA del plan)

**Prima di scrivere qualsiasi piano, fai tutte le domande necessarie all'utente.** Un piano basato su assunzioni è un piano che genererà retry inutili. Meglio 2 minuti di domande che 20 minuti di retry.

```
CLARIFICATION FLOW (obbligatorio per Tier 3+):

1. Analizza la richiesta dell'utente
2. Identifica TUTTE le informazioni mancanti o ambigue
3. Fai le domande — usa `clarify` tool o chiedi direttamente

DOMANDE OBBLIGATORIE (se l'info non è già nella richiesta):
  ├─ Architettura: "Preferisci monolite FastAPI o microservizi? DB SQLite o PostgreSQL?"
  ├─ Scope: "Vuoi solo backend o anche frontend? Se frontend, React/Vue/vanilla?"
  ├─ Autenticazione: "Serve auth? JWT, session, OAuth?"
  ├─ Database: "Quale DB? Schema esistente o da creare da zero?"
  ├─ API esterne: "Il sistema deve integrare API esterne? Quali?"
  ├─ Deploy target: "Dove vuoi deployare? Locale, Vercel, Docker, VPS?"
  ├─ Testing: "Vuoi test suite completa o solo smoke test?"
  ├─ Stile UI: (se frontend) "Hai preferenze di design? Colori, tema, riferimento a siti esistenti?"
  └─ Priorità: "Cosa è più importante: velocità di consegna o completezza? MVP o sistema production-ready?"

REGOLE DELLE DOMANDE:
  1. Non fare domande la cui risposta è già nella richiesta o nel codebase
  2. Non fare più di 5-6 domande in totale (batch in un unico messaggio, non una alla volta)
  3. Per ogni domanda, se possibile, suggerisci un default ragionevole (es. "DB: SQLite (default) o PostgreSQL?")
  4. Se l'utente risponde "fai tu" o "decidi tu" → usa i default e procedi senza altre domande
  5. Se il task è chiaro e completo → SALTA le domande, vai dritto al plan
  6. Per Tier 1-2: NON fare domande, il task è semplice enough
```

**Esempio di clarification interview reale:**

```
Utente: "Crea un sistema di prenotazione ristorante"

Prometheus Engine (Tier 3 rilevato → clarification):
  " Prima di iniziare, alcune domande per creare il piano migliore:
    1. DB: SQLite (default, semplice) o PostgreSQL (production)?
    2. Frontend: serve? Se sì, React (default) o altro?
    3. Auth: JWT (default) o session-based?
    4. Deploy: locale (default) o Docker/Vercel?
    5. Scope: MVP con prenotazioni + menu, o completo con recensioni + pagamenti?
    
    Rispondi anche solo con i numeri, es: '1=SQLite 2=React 3=JWT 4=locale 5=completo'
    Oppure dì 'fai tu' e uso i default. "

Utente: "1=SQLite 2=React 3=JWT 4=locale 5=completo"

→ Ora ho tutto per scrivere un piano preciso, zero assunzioni.
```

### 0.5b — Pianificazione

Dopo la clarification interview (o se il task è già completo di info):

```
if tier >= 3:
    └─ Carica skill `plan`
    └─ Esplora il codebase (read_file, search_files) per capire struttura esistente
    └─ Scrivi piano strutturato in .hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md
    └─ Usa il piano come input per la decomposizione (Phase 1)
```

### Cosa contiene il piano per prometheus-engine

Il piano NON sostituisce il loop — lo **alimenta**:
- **Architettura decisionale**: quale pattern, quali moduli, come comunicano
- **File inventory**: lista completa dei file da creare/modificare con path esatti
- **Interface contracts preliminari**: firme delle funzioni condivise tra moduli
- **Dipendenze tra task**: quali task devono finire prima che altri possano iniziare
- **Test strategy**: quali test, in che ordine, cosa coprono

### Flusso Plan → Prometheus Engine

```
1. Carica skill `plan`
2. Esplora codebase (read-only: read_file, search_files)
3. Scrivi .hermes/plans/<timestamp>-<slug>.md
   ├─ Goal + Architecture + Tech Stack
   ├─ Task list (bite-sized, 2-5 min cadauno)
   ├─ File paths esatti + codice copy-pasteable
   └─ Test + verification steps
4. Usa il piano come blueprint per Phase 1 (decomposizione)
   └─ Ogni task del piano → 1 subagente dispatchato
5. Procedi con Phase 2 (scatter) normalmente
```

**Regola d'oro:** Il piano è una guida, non una gabbia. Se durante lo streaming gather emerge che un task è più complesso del previsto, decomponilo ulteriormente al volo (Phase 3c — adaptive threshold tuning).

---

## Phase 1 — Massive Parallel Decomposition

### 1a — Decomposizione Dinamica (non fissa)

La decomposizione si adatta al numero di subagenti disponibili.
Implementazione reale: `scripts/prometheus_engine.py` → `fine_grained_decompose()`

```python
from prometheus_engine import fine_grained_decompose

# Iterazione 1: decomposizione aggressiva (molti task piccoli)
tasks = fine_grained_decompose(goal, available_subagents=50, iteration=0)

# Iterazioni successive: solo gap rimasti, più fine-grained
tasks = fine_grained_decompose(goal, available_subagents=50, iteration=1, gaps=failed_tasks)
```

**Esempio di decomposizione reale (API CRUD):**

```
GOAL: "API prenotazione ristorante con 4 entità"
SUBAGENTI: 50 disponibili

DECOMPOSIZIONE:
├── Modelli (5 task)
│   ├── models/restaurant.py     [1 file]
│   ├── models/reservation.py     [1 file]
│   ├── models/menu.py           [1 file]
│   ├── models/user.py           [1 file]
│   └── models/review.py         [1 file]
├── Routes (12 task)
│   ├── routes/restaurants.py    [1 file, 5 endpoint]
│   ├── routes/reservations.py   [1 file, 5 endpoint]
│   ├── routes/menu.py           [1 file, 4 endpoint]
│   ├── routes/auth.py           [1 file, 3 endpoint]
│   └── routes/search.py         [1 file, 1 endpoint]
├── Services (5 task)
│   ├── services/availability.py [1 file]
│   ├── services/notifications.py[1 file]
│   └── services/payments.py     [1 file]
├── Test (15 task)
│   ├── tests/test_restaurants.py[1 file, 5 test]
│   ├── tests/test_reservations.py [1 file]
│   └── ...
└── Docs (3 task)
    ├── README.md
    ├── docs/api.md
    └── docs/setup.md

TOTALE: 40 task, 40 file diversi ✓
CARICO BILANCIATO: max 5 file per subagente, media 1 file ✓
```

**Regole di scala:**

| Subagenti | Pattern di decomposizione |
|-----------|--------------------------|
| 1-5 | Task per file (model.py, routes.py, services.py, tests.py) |
| 5-15 | Task per funzione (ogni endpoint, ogni test suite, ogni helper) |
| 15-50 | Task per sotto-componente (User model, Auth routes, Validation, Test CRUD, Test Auth, Docs User, Docs Auth) |
| 50-100 | Task per riga logica + varianti multiple (User model v1, User model v2, Test variant A, Test variant B) |

### 1b — Pattern di Decomposizione per 100 Subagenti

Per sfruttare veramente 100 subagenti, uso pattern **multi-dimensionali**:

**Pattern A — Multi-Implementazione + Voting (per componenti critici)**
```
Task 1-5: 5 varianti di implementazione del modulo core (stessa spec, approccio diverso)
Task 6: Valutatore che sceglie la migliore variante
Task 7-N: task normali
```

**Pattern B — Ricerca + Implementazione + Test in parallelo**
```
Task 1-10: Ricerca esplorativa (10 angolazioni diverse)
Task 11-60: Implementazione (50 task atomici)
Task 61-80: Test paralleli (20 suite)
Task 81-90: Documentazione (10 sezioni)
Task 91-100: Review incrociata (10 peer review)
```

**Pattern C — Sistema Completo da Zero (full-stack)**
```
Task 1-5: Setup infrastructure (DB, auth, config, CI, deploy)
Task 6-20: Modelli e DB layer (15 entità)
Task 21-50: API routes (30 endpoint)
Task 51-70: Frontend components (20 componenti)
Task 71-85: Test (15 suite)
Task 86-95: Documentazione (10 sezioni)
Task 96-100: Integration review + deploy
```

| Pattern D — Data Pipeline Massiva
```
Task 1-20: Fetch dati da 20 fonti diverse
Task 21-40: Trasforma/normalizza ogni fonte
Task 41-60: Analizza/metriche su ogni dataset
Task 61-80: Merge e correla
Task 81-90: Genera report/visualizzazioni
Task 91-100: Review e quality check
```

> 💡 **Riferimenti utili:**
> - `references/external-api-integration.md` — pattern per integrare API esterne multiple con flag configurabili, gestione chiavi, e resilienza agli errori.
> - `references/weather-api-integration.md` — pattern specifico per progetti meteo: multi-source fetcher, arrotondamento a interi, ricerca web per contesto AI, esempi Meteoblue/Open-Meteo.
> - `references/ollama-integration.md` — pattern per chiamare Ollama con parsing JSON robusto, estrazione response, retry, subscription check.
> - `references/ai-response-caching.md` — pattern SHA256 per cache risposte AI (riduzione latenza 92%).
> - `references/ensemble-confidence-scoring.md` — blended confidence: 60% objective (ensemble agreement) + 40% subjective (AI self-assessment).
> - `references/climatology-3-level.md` — pattern per climatologia a 3 livelli (giorno esatto, ±5gg, mese): singola API call, 310 campioni vs 10, confidenza consolidata.
> - `references/int-to-float-precision.md` — pattern per convertire tutto lo stack da int a float con 1 decimale per betting Polymarket.
> - `references/benchmark-harness-pattern.md` — costruire benchmark harness per skill Hermes: SQLite metrics, verify_cmd ground truth, parser isolato, confronto multi-condizione (baseline/v1/v2).
> - `references/obsidian-vault-creation.md` — convertire una skill Hermes in vault Obsidian con wiki-link e graph view (MOC + note per fase + pattern reference).
> - `references/orchestrator-control.md` — controllo orchestrator per task corposi: gerarchia a 4 livelli (Parent→Orch→Leaf→Micro-worker), leaf dynamic split, 6 regole anti-bottleneck B1-B6, timeout allineati, context budget enforcement, error propagation.
> - `scripts/prometheus_engine.py` — modulo Python eseguibile con 10 funzioni reali (detect_band, fine_grained_decompose, calibrate, can_dispatch, quality_check, save/load pattern, cleanup_cache).
> - `scripts/e2e_test.py` — test end-to-end che simula 4 scenari reali (fix → media feature → sistema auth → full-stack). 35/35 checks.
> - `scripts/session_manager.py` — gestione sessioni lunghe: tracciamento stato, checkpoint automatico, quality trend, interrupt recovery. `SessionManager` classe Python.

### 1c — Shared Interface Contracts (pre-dispatch)

Prima di dispatchare subagenti che producono moduli chiamanti/chiamati tra loro (es. router.py → ollama_client.py), documenta esplicitamente le **firme complete delle funzioni condivise** nel context di OGNI subagente coinvolto.

**Regola:** se il subagente A deve chiamare una funzione del subagente B, la firma esatta di quella funzione (nome, parametri, tipi, sincrona o async, valori di ritorno) va inclusa nel context di ENTRAMBI — non solo in chi la implementa.

**Esempio di context block per interfaccia condivisa:**
```
--- CONTRATTO INTERFACCIA ---
Modulo chiamato: app/ollama_client.py (implementato da subagente B)

build_prompt(location: GeoResult, target_date: date,
             sources: list[SourceForecast],
             climatology: Optional[Climatology],
             days_ahead: int) -> str
  NOTA: funzione SINCRONA (no async/await) — il chiamante usa `prompt = build_prompt(...)`

call_ollama(prompt: str, max_retries: int = 3) -> OllamaForecast
  NOTA: funzione ASINCRONA — il chiamante usa `forecast = await call_ollama(...)`

check_ollama_status() -> OllamaStatus
  NOTA: funzione ASINCRONA

Modulo chiamante: app/router.py (implementato da subagente A)
  from ollama_client import call_ollama, build_prompt, check_ollama_status
  prompt = build_prompt(location=loc, target_date=d, sources=s, climatology=c, days_ahead=n)
  forecast = await call_ollama(prompt)
--- FINE CONTRATTO ---
```

**Perché è critico:** subagenti paralleli che implementano interfacce comunicanti senza contratto condiviso producono invariabilmente mismatch — un subagente usa `await build_prompt(...)`, l'altro definisce `def build_prompt(...)`; un subagente passa parametri posizionali, l'altro si aspetta keyword. Il contratto elimina il 90% di questi bug di integrazione **quando la decomposizione è nota prima del dispatch**.

**⚠️ Limite con dispatch dinamico:** poiché Phase 2a dispatcha in streaming mentre Phase 1a decompone dinamicamente, un contratto d'interfaccia per un modulo del Batch 2 potrebbe arrivare dopo che il Batch 1 è già stato scritto. In questo caso:
- **Se il contratto è noto prima del dispatch di entrambi:** includilo in entrambi i context → zero mismatch
- **Se il Batch 1 è già partito:** Batch 2 DEVE adattarsi alle firme già scritte da Batch 1 (leggi il file prodotto), non il contrario
- **Solo in Tier 3+ con pianificazione statica (Phase 0.5):** i contratti sono tutti noti in anticipo → vale la garanzia del 90%

### 1d — Quality Criteria Dinamici

Non uso più checklist fisse. Ogni task riceve quality criteria adattivi:

```python
def generate_criteria(task_type, tier, context):
    base_criteria = {
        "completeness": "Tutti i requisiti implementati senza stub",
        "correctness": "Funziona senza errori in condizioni normali",
        "edge_cases": "Gestisce input vuoti, null, duplicati, errori",
    }
    if task_type == "api":
        base_criteria.update({
            "status_codes": "200, 201, 400, 404, 409, 500 corretti",
            "validation": "Input validation presente per ogni campo",
            "tests": "Almeno 1 test per endpoint",
        })
    if task_type == "model":
        base_criteria.update({
            "constraints": "Unique, nullable, foreign key corretti",
            "repr": "__repr__ o __str__ presente",
            "migration": "Schema migrabile senza perdita dati",
        })
    if task_type == "ui":
        base_criteria.update({
            "responsive": "Funziona su mobile + desktop",
            "states": "Loading, empty, error, success gestiti",
            "no_slop": "No glassmorphism, gradienti viola, ombre soft generiche. Preferisci animazioni dinamiche, header che cambiano colore coi dati, grafici interattivi, e micro-interazioni.",
            "dynamic": "Header/sfondi/card cambiano in base ai dati (es. temperatura calda -> tema caldo). Colori narrativi, non decorativi.",
            "animations": "Transizioni fluide su cambi di stato, staggered entrance, skeleton loading animati, micro-interazioni hover/click.",
            "data_visuals": "Grafici interattivi (Recharts), gauge SVG animati, gradienti nelle barre — non solo numeri in grassetto.",
            "personality": "Quick-select per azioni frequenti, indicatori live (stato API/DB), tooltip informativi.",
        })
    return base_criteria
```

---

## Phase 2 — Autonomous Scatter (massive parallel dispatch)

### 2a — Streaming Dispatch (non più batch attendi-tutto)

Invece di fare un unico `delegate_task(tasks=[...])` e aspettare TUTTI i risultati, uso un approccio **streaming**:

```
┌─ Decomponi goal in 50 task
├─ Dispatch BATCH 1: task 1-25 (subagenti 1-25)
├─ Mentre BATCH 1 gira:
│   ├─ Prepara BATCH 2: task 26-50
│   ├─ Al primo risultato di BATCH 1 → valuta SUBITO
│   │   ├─ score >= threshold? → ✅ done
│   │   └─ score < threshold? → retry IMMEDIATO (senza aspettare)
│   ├─ Dispatch BATCH 2: task 26-50
│   └─ Continua a processare risultati in streaming
└─ I retry si mischiano naturalmente col flusso
```

**Vantaggio:** non c'è mai un "tempo morto" tra batch. I retry partono mentre gli altri task girano ancora.

**⚠️ Limite di safety:** lo streaming dispatch è il default, MA ogni batch DEVE passare `can_dispatch()` (Phase 3e) prima di partire. Se il context budget è a rischio, il batch viene ridotto automaticamente — NON sospende lo streaming, ma lancia batch più piccoli fino a quando il budget non si libera. La regola "20-25 in-flight" di Phase 3e è un **warning threshold**, non un hard stop. In caso di conflitto: Phase 3e vince su Phase 2a (Regola di Precedenza).

### 2b — Subagent Prompt Template (auto-consapevole)

Ogni subagent sa che fa parte di un loop più grande:

```
TASK: {description}
YOUR ID: {task_id}
QUALITY THRESHOLD: {threshold}/10
MAX_INTERNAL_ITERATIONS: 3

QUALITY CRITERIA:
{custom_criteria}

SELF-AWARENESS:
You are one of {total_tasks} parallel agents working on {goal_name}.
Others are working on related but non-overlapping files.
Your work will be evaluated automatically when you return.
If you score below threshold, you WILL be retried with feedback.

INSTRUCTIONS:
1. Implement the task completely (no stubs, no TODO, no pass)
2. Self-verify against quality criteria
3. If below threshold, fix and re-verify (max 3 tries)
4. If still below threshold after 3 tries, return honest score + gaps

RETURN FORMAT (MANDATORY at end):
## RESULT
- task_id: {task_id}
- status: pass|fail|partial
- quality_score: N/10
- gaps: [specific gaps if any]
- files_created: [paths]
- notes: [anything I should know]
```

### 2c — Pre-Dispatch Validation

Prima di dispatchare, verifico che il batch sia valido:

```
PRE-FLIGHT CHECKLIST:
□ Ogni task ha file NON CONDIVISO? I singoli task non devono toccare file condivisi (router principale, __init__.py, config, requirements.txt).
   └─ 🌉 **Assembly Task**: i file condivisi sono modificati SOLO da un task post-batch dedicato, dopo che tutti i task individuali sono verificati
□ Ogni task ha quality criteria specifici?
□ Il carico è bilanciato? (nessun task > 2× media)
□ Il numero di task <= subagents_available?
□ Ho template di retry pronti per fallimenti rapidi?
□ Ho salvato i criteri di successo per il final report?
□ **Firme interfacce**: se due task producono moduli che si chiamano tra loro, ho incluso il contratto delle funzioni (nomi, parametri, sincrono/async) in ENTRAMBI i context?
□ **Assembly task pianificato?** Ho identificato i file condivisi che devono essere aggiornati dopo il batch e allocato un assembly task?
```

### 2d — Esempio di Dispatch Reale

```python
# Dispatch per sistema prenotazione ristorante (40 task)
delegate_task(tasks=[
    {
        "goal": "Crea modello Restaurant con campi: name, address, phone, cuisine_type, created_at",
        "context": f"TASK: models/restaurant.py\nQUALITY THRESHOLD: 7/10\n...",
        "toolsets": ["terminal", "file"]
    },
    {
        "goal": "Crea endpoint CRUD per Restaurant (GET/POST/PUT/DELETE /api/restaurants)",
        "context": f"TASK: routes/restaurants.py\nQUALITY THRESHOLD: 7/10\n...",
        "toolsets": ["terminal", "file"]
    },
    # ... 38 altri task
])
```

### 2e — Orchestrator Dispatch (Tier 3-4, task corposi)

Per task con 10+ sub-task su 3+ sotto-sistemi, usa orchestrator invece di dispatch diretto.

**Architettura a 4 livelli:**
```
Parent → Orchestrator → Leaf → Micro-worker (max 2, solo se leaf valuta task troppo complesso)
```

**Quando usare orchestrator:**
- 10+ task su 3+ aree distinte → 1 orchestrator per area
- Sistema full-stack (>50 file, codebase sconosciuto)
- Task che richiede ricerca + implementazione coordinata

**Quando NON usare:**
- Tier 1-2 (sempre dispatch diretto)
- Codebase conosciuto (familiarità alta → 0 subagenti)
- <10 task (dispatch diretto più efficiente)

**6 regole anti-bottleneck (B1-B6)** — vedi `references/orchestrator-control.md` per dettaglio completo:
- **B1**: Mini-batch da max 5 leaf (non tutti insieme)
- **B2**: Depth auto-limit per Tier (T1-2→1, T3→2, T4→3 solo se >50 file)
- **B3**: Context snapshot <200 token iniettato in ogni subagente
- **B4**: Retry degradazione forzata (retry 2 = inline, retry 3 = orchestrator inline)
- **B5**: Timeout allineati (micro 60s → leaf 120s → orch 240s → parent 300s)
- **B6**: `can_dispatch()` preventivo OBBLIGATORIO prima di ogni batch

**Leaf Dynamic Split:** un leaf che valuta il task troppo complesso (3+ file con dipendenze, stima >120s) può spawnare MAX 2 micro-worker. Il micro-worker è dead-end (non può spawnare). Context snapshot iniettato. Se entrambi falliscono → leaf implementa inline (B4).

---

## Phase 3 — Streaming Quality Gate (the real innovation)

Questa è la fase che rende v3 veramente autonoma. **Non aspetto. Processo subito.**

### 3a — Il Loop Streaming

```
while goal_not_achieved AND iteration < max_iterations:
    ┌─ Arriva risultato da subagente X
    ├─ PARSE: estrai status, quality_score, gaps, files
    ├─ VALIDATE: i files_created esistono davvero? (stat/check)
    │
    ├─ if score >= threshold:
    │   ├─ ✅ tasks_completed.append(X)
    │   ├─ GIT CHECKPOINT: se i file di X sono verificati e non ci sono
    │   │   task in-flight che modifichino gli stessi file:
    │   │   └─ git add <files_di_X> && git commit -m "feat: <task_desc>"
    │   │       └─ git push (se remoto configurato)
    │   └─ continue (aspetto prossimo risultato)
    │
    ├─ if score < threshold AND iteration < max_iterations:
    │   ├─ ❌ Prepara retry per X IMMEDIATAMENTE
    │   ├─ Feedback: "Hai fatto {gaps}. Correggi: {fix_hint}"
    │   ├─ dispatch_retry(X)  # parte SUBITO, non aspetta altri
    │   └─ tasks_in_flight.append(X)
    │
    ├─ if score < threshold AND iteration >= max_iterations:
    │   ├─ ⚠️ Raggiunto tetto di sicurezza. Vai a Phase 7 (Escalation Ladder).
    │   ├─ NON accettare automaticamente: l'utente decide se accettare, skippare o fix manuale.
    │   └─ Salva in self_lessons per analisi future
    │
    ├─ UPDATE: ricalcola first_pass_rate, avg_quality
    │
    └─ if ALL tasks accounted for (completed + in_flight == total):
        └─ if tasks_completed.size == total:
            └─ 🎉 GOAL ACHIEVED → final report
```

### 3a-bis — Git Commit+Push Policy (OBBLIGATORIA)

L'utente vuole commit+push dopo ogni modifica riuscita. Il loop lo codifica così:

```
GIT CHECKPOINT RULES:
1. Dopo che un task PASSA il quality gate (score >= threshold) e i file sono validati:
   └─ Se i file del task sono ESCLUSIVI (non condivisi) → git add + commit + push immediato
   └─ Se i file del task includono file CONDIVISI → ATTENDI: il commit dei file condivisi avviene SOLO nell'assembly task post-batch
2. NON commitare file di task ancora in-flight (conflitti potenziali)
3. Se due task completati modificano file ESCLUSIVI (nessun overlap con file condivisi):
   └─ Commit separati, push in sequenza
4. Commit message in italiano, formato conventional commits:
   └─ feat: aggiungi modello Restaurant
   └─ fix: correggi validazione date prenotazione
   └─ test: aggiungi test endpoint /api/restaurants
5. Se git push fallisce (rete, auth):
   └─ Retry singolo, poi continua il loop (commit resta locale)
   └─ Segnala nel final report: "N commit non pushati"
6. 🌉 ASSEMBLY TASK: dopo che TUTTI i task del batch sono verificati, un assembly task dedicato:
   └─ Modifica i file condivisi (router, __init__.py, config, requirements.txt) per integrare i nuovi moduli
   └─ Fa commit + push dei file condivisi
   └─ Questo è l'unico task autorizzato a toccare file condivisi
```

**Perché nel loop e non alla fine:** commit granulari dopo ogni task passato = rollback possibile per singolo task se un task successivo lo rompe. Commit unico finale = all-or-nothing.

### 3b — Esempio di Streaming in Azione

```
LINEA DEL TEMPO (minuti:secondi):

0:00 — Dispatch 50 task
0:45 — Arriva task 1 (models/restaurant.py) → score 8/10 ✅
0:48 — Arriva task 2 (routes/reservations.py) → score 4/10 ❌
0:49 — RETRY task 2: "Manca validazione date, conflitto orari, test assenti"
0:52 — Arriva task 3 (models/user.py) → score 9/10 ✅
1:05 — Arriva task 4 (services/notifications.py) → score 5/10 ❌
1:06 — RETRY task 4: "Manca fallback email, template notifica, test"
1:15 — Arriva RETRY task 2 (secondo tentativo) → score 8/10 ✅
1:22 — Arriva RETRY task 4 (secondo tentativo) → score 7/10 ✅
1:30 — Arriva ultimo task originale → score 9/10 ✅
1:30 — TUTTI I TASK CONTABILIZZATI → convergenza
     └─ 48 pass al primo tentativo (96%)
     └─ 2 retry immediati, entrambi convergenti
     └─ Qualità media: 8.4/10

TEMPO TOTALE: 1 min 30s (invece di ~3 min con batch-retry)
```

### 3c — Adaptive Threshold Tuning (solo per il prossimo batch)

Se vedo che troppi task falliscono, **aggiusto la decomposizione per il batch successivo** (NON per i task già dispatchati):

```
MONITOR:
if first_pass_rate (after 25% of tasks) < 60%:
    └─ "Decomposizione troppo grossolana per questi task"
    └─ Per il PROSSIMO batch: raddoppia la granularità (split ogni task in 2)
    └─ I task già in volo completano con granularità originale
    └─ Salva lezione: "Task di tipo X richiedono decomposizione più fine"

if first_pass_rate (after 25% of tasks) > 90%:
    └─ "Decomposizione troppo fine, overhead eccessivo"
    └─ Per il PROSSIMO batch: merge adiacenti
    └─ I task già in volo completano con granularità originale
    └─ Salva lezione: "Task di tipo X possono essere aggregati"
```

> **⚠️ Regola importante:** NON cambiare mai granularità ai task già dispatchati. Rischierebbe sovrapposizioni e conflitti con task "vecchio stile" ancora in esecuzione.

### 3d — Validazione File Fisici

Ogni risultato viene validato fisicamente:

```
VALIDATE RESULT:
1. read_file(task.files_created[0]) — esiste? → se no, ❌ fail aggiuntivo
2. grep -n "TODO\\|pass\\|stub" task.files_created — codice morto?
3. python -c "from task.module import ..." — sintassi ok?
4. wc -l task.files_created — file non vuoto?

Se validazione fisica fallisce → fail immediato (anche se score era alto)
```

### 3e — Context Window Protection (CRITICO per Tier 3-4)

Quando dispatchi 30-100 subagenti, ogni subagente restituisce un summary. **100 summary simultanei possono saturare la context window del parent** e far crashare la sessione o triggerare compression death spiral.

**Protezione attiva (Hermes built-in):**
- `delegation.max_summary_chars: 24000` — hard cap per summary
- Dynamic headroom budget — Hermes calcola lo spazio rimanente e trimma automaticamente
- Spill su file — summary troncati vanno in `~/.hermes/cache/delegation/` con offset per read_file

**Protezione attiva (prometheus-engine — DA SEGUIRE SEMPRE):**

```
CONTEXT BUDGET RULES:
1. Prima di dispatchare un batch grande (Tier 3+):
   ├─ Calcola context budget: context_length - (system_prompt + conversation_so_far)
   ├─ Stima summary size: N_subagenti × ~2000 token media per summary
   └─ Se N_subagenti × 2000 > context_budget × 0.6:
      └─ ⚠️ TROPPI SUBAGENTI PER IL CONTEXT RIMANENTE
      └─ Riduci il batch size (dispatcha in 2-3 ondate, non tutte insieme)
      └─ Oppure riduci summary target: istruisci subagenti a summary <500 token

2. Dispatch a ondate (se batch > 20 subagenti):
   ├─ Ondata 1: task 1-20 → raccogli risultati → processa → libera context
   ├─ Ondata 2: task 21-40 → raccogli → processa → libera context
   └─ Ondata 3: task 41-N → ...
   └─ ⚠️ Warning threshold: oltre 20-25 subagenti in-flight simultanei con summary >1000 token rischia saturazione. Riduci batch se can_dispatch() segnala rischio (Phase 2a + Regola di Precedenza).

3. Summary compression proattiva:
   ├─ Per Tier 2: summary <500 token (3-5 righe)
   ├─ Per Tier 3: summary <1000 token (5-10 righe)
   └─ Per Tier 4: summary <2000 token (10-20 righe)
   └─ Istruisci ogni subagente: "Ritorna un summary CONCISO. Massimo N righe."

4. Compression death spiral prevention:
   ├─ Se context compression triggera 2+ volte in una sessione:
   │   └─ ⚠️ CONTEXT SATURATO — riduci subagenti o summary size
   │   └─ Passa a dispatch a ondate più piccole
   └─ Non ignorare i trigger di compression — sono un segnale di overflow
```

**Costo reale di ignorare questo:** se 100 summary saturano il context, Hermes comprime → perde contesto dei task già completati → retry duplicano task già fatti → altri summary → overflow di nuovo → death spiral → sessione crasha o produce qualità pessima.

---

## Phase 4 — Self-Learning Loop (the moat)

### 4a — Deep Pattern Capture (Token-Optimized)

Il self-learning profondo ha **3 livelli** di persistenza, ognuno con un trade-off diverso tra ricchezza e consumo di token:

#### Livello 1 — Memory Entry Compressa (ultimo batch della sessione)

Entry breve e densa, iniettata in ogni sessione futura. **Massimo 200 caratteri** per non sprecare context.

**QUANDO salvare:** solo dopo l'ULTIMO batch completato nella sessione (non dopo ogni batch). Questo rispetta il Guardrail 8 (max 3 memory entry per sessione). Se la sessione ha 1 batch → 1 entry. Se ha 5 batch → 1 entry (l'ultimo, con metriche aggregate di tutta la sessione).

```python
memory(action="add", target="memory", content=(
    f"PE[{goal_type}|T{tier}] FPR={first_pass_rate:.0%} dec={decomposition_pattern} "
    f"q={avg_quality:.1f} iter={convergence_iterations} "
    f"L: {'; '.join(lessons[:2])}"  # max 2 lessons, più impactful
))
```

**Esempio reale (156 chars):**
```
PE[api_crud|T3] FPR=84% dec=per_endpoint q=8.7 iter=3 L: servizi FPR<API; per_file ok fino a 30 task
```

**Perché compresso:** il memory store è limitato (2200 char totali). Entry verbose riempiono il budget velocemente. Entry compresso = più lezioni salvabili = apprendimento più ampio.

#### Livello 2 — Pattern Cache File (per pattern riusciti, FPR > 70%)

Pattern dettagliati salvati in un file JSON locale. **Non iniettato in context** (zero token cost), ma consultabile on-demand quando serve.

Implementazione reale: `scripts/prometheus_engine.py` → `save_pattern()` / `load_pattern()` / `cleanup_cache()`

```python
from prometheus_engine import save_pattern, load_pattern, cleanup_cache

# Salva pattern dopo un batch completato
save_pattern(
    goal_type="api_crud",
    tier=3,
    decomposition_pattern="per_endpoint",
    first_pass_rate=0.84,
    avg_quality=8.7,
    subagent_count=10,
    task_count=40,
    lessons=["servizi FPR<API", "per_file ok fino a 30 task"],
)

# Recall: carica pattern matching prima di decomporre
pattern = load_pattern(goal_type="api_crud", min_fpr=0.8)
if pattern:
    # Usa come template, risparmia ~2000 token di reasoning
    decomposition = pattern["decomposition_pattern"]

# Cleanup (Guardrail 5): ogni 10 batch
cleanup_cache(max_entries=20, min_fpr=60)
```

**Quando consultare la cache:** all'inizio di Phase 1 (decomposizione), se il goal_type corrisponde a un pattern in cache, carica quel pattern invece di decomporre da zero:

```
PHASE 1 START:
  ├─ Leggi pattern_cache.json
  ├─ Cerca entry con goal_type matching
  ├─ Se trovata con FPR > 80%:
  │   └─ Usa quella decomposizione come template
  │   └─ Adatta nomi file/specifiche al goal corrente
  │   └─ SALTA la decomposizione creativa (risparmio ~2000 token di reasoning)
  └─ Se non trovata o FPR < 80%:
      └─ Decomposizione da zero (normale)
```

**Risparmio token stimato:** 1500-3000 token per sessione quando un pattern matching esiste, perché non devo "reinventare" la decomposizione.

#### Livello 3 — Skill Dedicata (pattern ricorrente, 3+ occorrenze)

Se lo stesso goal_type appare 3+ volte con FPR > 75%, il pattern è stabile e merita una skill:

```python
# Dopo 3+ occorrenze di stesso pattern
skill_manage(
    action="create",
    name=f"pattern-{goal_type}",
    category="software-development",
    content=generate_skill_from_pattern(pattern_data)
)
```

**Vantaggio:** le skill caricate con `skill_view` sono strutturate e ottimizzate, molto più ricche di una memory entry ma più efficienti di reasoning ad-hoc. Quando il pattern è stabile, la skill lo codifica permanentemente.

### 4b — Token-Efficient Recall (PRIMA del loop)

All'inizio di ogni sessione di coding, prima di Phase 0, esegui un **recall rapido**:

```
RECALL SEQUENCE (30 secondi, ~500 token):

1. Memory injection (automatica, zero cost extra)
   └─ Le entry PE[...] sono già nel context
   └─ Scan: ci sono pattern matching per questo goal_type?

2. Pattern cache check (1 read_file call)
   └─ read_file(hermes_home + "/pattern_cache.json")
   └─ Path: ~/AppData/Local/hermes/ su Windows, ~/.hermes/ su Linux/Mac
   └─ Match per goal_type? → usa come template

3. Skill list check (1 skills_list call)
   └─ Esiste già skill "pattern-{goal_type}"?
   └─ Se sì → caricala con skill_view (struttura ottimizzata)
```

**Risparmio token complessivo:**
- Senza recall: decomposizione creativa + reasoning = ~3000-5000 token
- Con recall + match trovato: adattamento template = ~800-1200 token
- **Risparmio: 60-75% token di planning, stessa qualità output**

### 4c — Adaptive Calibration (con memoria storica)

Adatto i parametri basandomi sulla storia persistente.
Implementazione reale: `scripts/prometheus_engine.py` → `calibrate()`

```python
from prometheus_engine import calibrate

# Leggi history dal pattern cache
history = load_pattern(goal_type="api_crud")  # ritorna lista di entry

params = calibrate("api_crud", history)
# params = {"granularity": "fine", "threshold": 6.5, "subagents": None, "extra_criteria": [...]}
```

### 4d — Lesson Hierarchy (quali lezioni salvare)

Non tutte le lezioni hanno lo stesso valore. Prioritizza:

```
PRIORITÀ LESSON (salva solo le top 2-3 per batch):

P0 — Structural (sempre salva):
  "Decomposizione per_file non funziona per task con dipendenze circolari"
  → Cambia la strategia di decomposizione futura

P1 — Task-specific (salva se ricorrente):
  "Task di servizi (notifiche/pagamenti) hanno FPR più basso del 20%"
  → Aggiungi quality criteria extra per servizi

P2 — Context-specific (salva se progetto ricorrente):
  "FastAPI route ordering: route statiche prima di /{param}"
  → Pitfall da verificare in progetti FastAPI simili

P3 — One-off (NON salvare, logga solo in STATE):
  "Il modulo XYZ aveva un typo nel nome"
  → Non è una lezione, è un incidente isolato
```

**Regola:** salvare tutto = memory overflow + lezioni inutili che affogano quelle utili. Meno ma meglio.

### 4e — Self-Learning Feedback Loop

Il ciclo completo di apprendimento:

```
Sessione N:
  ├─ RECALL: leggi pattern cache + memory → usa template se match
  ├─ EXECUTE: loop prometheus-engine con parametri calibrati
  ├─ CAPTURE: salva pattern (Livello 1 memory + Livello 2 cache)
  └─ CALIBRATE: aggiorna parametri per prossimo uso
      │
      ▼
Sessione N+1:
  ├─ RECALL: trova pattern della sessione N → adatta
  ├─ EXECUTE: con parametri calibrati → FPR dovrebbe essere più alto
  ├─ CAPTURE: confronta con sessione N, salva delta
  └─ CALIBRATE: raffina ulteriormente
      │
      ▼
Sessione N+3:
  └─ Se pattern stabile (FPR > 75% per 3 volte) → crea skill (Livello 3)
      └─ Ora il pattern è permanentemente codificato
      └─ Recall usa skill_view invece di cache file (più ricco, più strutturato)
```

**Misurabile:** il first-pass rate DEVE aumentare nel tempo. Se dopo 5 sessioni dello stesso goal_type il FPR non è migliorato di almeno 10%, il self-learning non sta funzionando — rivaluta il formato delle lezioni.

### 4f — Self-Learning Guardrails (CRITICO — previene inquinamento)

Il self-learning autonomo **senza guardrail è pericoloso**. Il modello che impara dai propri output può entrare in cicli di feedback negativi, accumulare lezioni sbagliate, degradare le skill, e saturare il memory store. Questi guardrail sono **non-opzionali**.

#### Guardrail 1 — Memory Budget Cap

Il memory store è 2200 char totali. Senza cap, si riempie e sovrascrive entry utili.

```
PRIMA di salvare una memory entry:
  ├─ Conta quante entry PE[...] esistono già nel memory store
  ├─ Se > 8 entry PE[...]:
  │   └─ Trova la entry PE[...] più vecchia con FPR più basso
  │   └─ Sostituiscila (memory action="replace", old_text=<substring>)
  │   └─ NON aggiungere — sostituisci
  ├─ Se <= 8 entry PE[...]:
  │   └─ Aggiungi nuova entry
  └─ Mai superare 10 entry PE[...] totali nel memory store
```

**Regola d'oro:** entry PE[...] nuove sostituiscono entry PE[...] vecchie e peggiori. Non si accumulano.

#### Guardrail 2 — Lesson Validation (anti-circolarità)

Il modello non può validare le proprie lezioni con se stesso (bias di conferma). Una lezione è valida SOLO se:

```
LESSON VALIDATION CRITERIA:
  ✅ Valid (salva):
     ├─ La lezione è confermata da un test fallito + fix riuscito (evidence-based)
     ├─ La lezione è un pitfall tecnico verificabile (es. "FastAPI route ordering")
     └─ La lezione proviene da un post-mortem con root cause identificata
  
  ❌ Invalid (NON salvare — rischio circolarità):
     ├─ "Ho provato X e ha funzionato" — non è una lezione, è un'anecdota
     ├─ "Il modello X è migliore del modello Y" — opinione, non fatto
     ├─ Lezioni che si autoriferiscono (es. "salva lezioni frequentemente")
     └─ Lezioni che non hanno un criterio di verifica oggettivo
```

**Test anti-circolarità:** prima di salvare una lezione, chiediti: "Se questa lezione fosse sbagliata, come lo saprei?" Se non hai una risposta, non salvarla.

#### Guardrail 3 — Skill Mutation Protection

L'prometheus-engine può patchare le skill, ma con limiti rigidi:

```
SKILL MUTATION RULES:
  ✅ Permesso:
     ├─ Patch pitfalls section (aggiungere un nuovo pitfall scoperto)
     ├─ Patch riferimenti (aggiungere un reference file)
     └─ Patch esempi (aggiornare esempi obsoleti)
  
  ⛔ Vietato (senza conferma utente):
     ├─ Modificare la Philosophy section
     ├─ Modificare i Tier thresholds
     ├─ Modificare le Quality criteria base
     ├─ Cancellare fasi del loop (Phase 0-10)
     └─ Modificare gli stessi guardrail (meta-modifica)
  
  📋 Procedura per mutazioni permesse:
     1. Backup: copia la sezione originale in un commento nel file
     2. Patch: applica la modifica
     3. Verify: ricarica la skill con skill_view e verifica coerenza
     4. Log: salva in memory "AP skill patch: <cosa cambiato e perché>"
     5. Max 1 patch per sessione (no batch mutation)
```

#### Guardrail 4 — Skill Proliferation Cap

Non creare skill infinite. Hard limits:

```
SKILL CREATION LIMITS:
  ├─ Max 5 skill pattern-* totali (oltre il limite → offri all'utente di consolidarle)
  ├─ Prima di creare skill pattern-X, verifica che non esista già una skill simile
  ├─ Se 2 skill pattern-* hanno goal_type simile > 70% → CONSOLIDALE in una
  ├─ Max 1 skill creata per sessione (no批量 creation)
  └─ Ogni skill pattern-* deve avere un "last_used" timestamp — se non usata in 30 giorni → archiviala
```

#### Guardrail 5 — Pattern Cache Cleanup

Il pattern_cache.json cresce indefinitamente senza cleanup:

```
PATTERN CACHE MAINTENANCE (ogni 10 batch completati):
  ├─ Leggi pattern_cache.json
  ├─ Conta entry totali
  ├─ Se > 20 entry:
  │   └─ Ordina per timestamp
  │   └─ Rimuovi le 5 più vecchie (salva i loro pattern come memory entry compressa prima di rimuovere)
  ├─ Se > 50 entry:
  │   └─ EMERGENZA: rimuovi tutte tranne le 10 più recenti con FPR > 70%
  └─ Se un goal_type ha 3+ entry con FPR < 60%:
      └─ Elimina quel goal_type dalla cache — il pattern non funziona
```

#### Guardrail 6 — Project Isolation (anti-contamination)

Le lezioni di un progetto NON devono contaminare progetti diversi:

```
PROJECT ISOLATION RULES:
  ├─ Le lezioni tecniche specifiche (es. "FastAPI route ordering") sono GLOBALI — valide ovunque
  ├─ Le lezioni architetturali (es. "usa SQLite raw queries") sono PROGETTO-SPECIFICHE
  │   └─ Marca con prefisso: PE[api_crud|PolimarketWeather|T3]...
  │   └─ Durante recall, matcha solo se il progetto corrente è lo stesso
  ├─ Le lezioni di stile UI sono PROGETTO-SPECIFICHE (ogni progetto ha il suo design)
  └─ Se il progetto corrente non matcha nessun entry di progetto → non usare quelle entry
```

**Implementazione pratica:** nel salvare una memory entry, includi il nome del progetto (dal cwd o dal git remote) se la lezione è progetto-specifica. Nel recall, filtra per progetto prima di applicare.

#### Guardrail 7 — Human Checkpoint (no fully autonomous skill mutation)

Il modello NON può creare, modificare, o cancellare skill in modo completamente autonomo. Sempre:

```
HUMAN CHECKPOINT per skill operations:
  ├─ skill_manage(action="create") → chiedi conferma all'utente prima
  ├─ skill_manage(action="delete") → chiedi conferma all'utente SEMPRE
  ├─ skill_manage(action="edit") → solo se l'utente ha approvato in questa sessione
  ├─ skill_manage(action="patch") → permesso per pitfalls/references (Guardrail 3), ma:
  │   └─ Notifica l'utente: "Ho patchato <skill> per <motivo>"
  └─ skill_manage(action="write_file") → come patch, notifica dopo
```

**Il self-improvement è autonomo nel DETECT (cosa imparare), ma collaborativo nel ACT (cosa modificare).** Il modello identifica pattern e lezioni da solo, ma le modifiche strutturali alle skill richiedono consenso umano. Questo è coerente con la filosofia della skill: **"Autonomous in execution, collaborative in mutation"** — il loop decide, esegue e ritenta senza fermarsi, ma le mutazioni permanenti al sistema (skill, guardrail, flusso) passano dall'utente.

#### Guardrail 8 — Session Memory Flush Cap

Per evitare che una singola sessione lunga accumuli troppi aggiornamenti di memoria:

```
SESSION MEMORY CAP:
  ├─ Max 3 memory entry PE[...] per sessione
  ├─ Max 1 memory entry PostMortem[...] per sessione  
  ├─ Max 1 skill patch per sessione
  ├─ Max 1 pattern_cache.json update per sessione (ultimo batch solo)
  └─ Se la sessione produce più dati di questi:
      └─ Salva solo i top-N per impatto (ordina per severity × FPR delta)
      └─ Gli altri vai nel final report come "lessons not persisted (cap reached)"
```

#### Guardrail 9 — Drift Detection

Rileva se il self-learning sta degradando invece di migliorare:

```
DRIFT DETECTION (ogni 5 sessioni dello stesso goal_type):
  ├─ Confronta FPR delle ultime 5 sessioni vs le 5 precedenti
  ├─ Se FPR medio è sceso di > 10%:
  │   └─ ⚠️ DRIFT DETECTED — il self-learning sta peggiorando
  │   └─ Azioni:
  │       ├─ Smetti di salvare nuove lezioni per questo goal_type
  │       ├─ Segnala all'utente: "Il pattern per X sta degradando, lezioni sospette"
  │       └─ Proponi reset delle lezioni per quel goal_type
  └─ Se FPR medio è stabile o migliorato:
      └─ ✅ Self-learning sano, continua
```

#### Guardrail 10 — Transparency Log

Ogni operazione di self-learning deve essere tracciabile:

```
SELF-LEARNING LOG (nel final report di ogni sessione):
  ├─ Memory entries salvate: N (di cui N sostituite)
  ├─ Pattern cache: aggiornata/non aggiornata (ragione)
  ├─ Skill patched: sì/no (quale, cosa, perché)
  ├─ Skill create: sì/no (quale, con conferma utente?)
  ├─ Lesson validation: N validate, N scartate (ragione scarto)
  └─ Guardrail attivati: lista dei guardrail che hanno limitato operazioni
```

**L'utente deve sempre sapere cosa è stato imparato, cosa è stato modificato, e cosa è stato bloccato.**

---

## Phase 5 — Scale Patterns (come usare veramente 100 subagenti)

### Pattern 1: Micro-Task Cascade (50-100 subagenti)

Per progetti grandi, decomponi ogni file in task per singola funzione.

### Pattern 2: Multi-Variant + Selection (30-50 subagenti)

Per componenti critici dove la qualità è fondamentale:
- 5 varianti di implementazione dello stesso modulo
- 1 valutatore che sceglie la migliore
- Task normali per il resto

### Pattern 3: Exploration Sprint (100 subagenti)

Per esplorazione/ricerca massiva: ogni subagente esplora un'angolatura diversa.

### Pattern 4: Full System Build (80-100 subagenti)

MVP da zero: backend, frontend, test, docs, deploy in parallelo.

---

## Phase 6 — Retry Intelligence

### 6a — Tipi di Retry

| Tipo | Score | Causa tipica | Strategia retry |
|------|-------|-------------|-----------------|
| **SUPERFICIALE** | 5-6 | Quality criteria non letti | Stesso task + feedback specifico |
| **STRUTTURALE** | 3-4 | Approccio sbagliato | Task ridefinito + hint architetturale |
| **GRAVE** | 0-2 | Task mal specificato | Riscrivi task da capo, decomponi in 2-3 micro-task |
| **SILENZIOSO** | N/A | Subagente non torna (timeout) | Pivota inline: implementa TU il task |

### 6b — Feedback Arricchito per Retry

```
v2 feedback: "Mancano gli edge case"
v3 feedback: "Mancano 3 edge case specifici: (1) email duplicata → 409,
              (2) campo vuoto → 400, (3) utente non trovato → 404.
              Aggiungi test per ognuno. Il resto del codice è ok (score 6→8)."
```

### 6c — Limite di Retry Intelligente (convergenza osservata + tetto di sicurezza)

La regola primaria è la **convergenza osservata**. Il contatore `max_iterations` esiste solo come **tetto di sicurezza** (per evitare loop infiniti), non come regola decisionale:

- Se dopo retry quality_score migliorato di >= 2 punti → continua (sta convergendo)
- Se migliorato < 2 punti → cambia strategia (split task, hint più specifici)
- Se PEGGIORATO → ferma retry, riparti da zero con task più piccolo
- Se `iteration >= max_iterations` E il delta è < 2 → **escala a Phase 7** (l'utente decide)

> **Coerenza con Phase 3a:** quando 3a rileva `iteration >= max_iterations`, NON accetta automaticamente ma attiva l'Escalation Ladder. In caso di conflitto tra questa regola e Phase 3a, vince la Regola di Precedenza → escalation all'utente.

---

## Phase 7 — Failure Escalation Ladder

Quando un task non converge, seguo questa scala:

```
1. SELF-VERIFY (subagente) — fallito
    ↓
2. RETRY CON FEEDBACK (io) — fallito
    ↓
3. CHANGE STRATEGY (io) — split task, hint architetturale — fallito
    ↓
4. ESCALATE TO USER — "Task X non converge dopo N iter.
    Quality score: Y/10. Gap residui: [specifici]. Come procedo?"
    ↓
5. USER DECIDE — skip? fix manuale? accetta con gap?
```

**Regola:** Non arrivo mai al punto 4 senza aver provato almeno 3 strategie diverse.

---

## Phase 8 — Final Report + Self-Learning

### 8a — Report Strutturato

```
## ✅ Completato: [Goal]

### Loop Efficiency
├─ Subagenti usati: N / M disponibili
├─ First-pass rate: XX% (batch 1)
├─ Convergenza: X iterazioni
├─ Qualità media finale: X.Y/10
├─ Streaming retry: X immediati, Y batch
└─ Durata totale: X min

### Self-Learning
├─ Pattern salvato: decomposizione [pattern] (funziona XX% first-pass)
├─ Lesson: [lezione appresa]
├─ Calibrazione: [modifiche ai parametri]
└─ Skill: prometheus-engine v4.0.0

### Quality Summary
├─ ✅ Task completati: X/Y
├─ ⚠️ Task con gap accettati: X
└─ ❌ Task escalati all'utente: X (se applicabile)

### Self-Feedback
├─ Autovalutazione: XX/100
└─ Note: [punti di forza e miglioramento]
```

### 8b — Self-Learning Actions

Sempre al termine:
1. Salva pattern di decomposizione (se first-pass > 80%)
2. Salva lesson se first-pass < 60%
3. Aggiorna calibrazione automatica per prossimo uso
4. Se 3 pattern simili di successo → offri all'utente di creare una skill dedicata

---

## Phase 9 — Complete Quality Matrix

Implementazione reale: `scripts/prometheus_engine.py` → `quality_check()`

```python
from prometheus_engine import quality_check

# Enforcement automatico dopo ogni task
result = quality_check(
    files_created=["backend/app/routes.py", "backend/app/models.py"],
    task_type="api",
)
# result = {"passed": True/False, "checks": [...], "failures": [...]}
# Se passed=False → retry immediato con feedback sui failures
```

### Verifica completa — E2E Integration Test

```bash
# Test rapido (4 scenari, 35 checks)
python scripts/e2e_test.py

# Test verboso (output dettagliato per ogni step)
python scripts/e2e_test.py --verbose
```

L'E2E test copre:
- ✅ 4 scenari: fix rapido, feature media, sistema auth, full-stack e-commerce
- ✅ Tutte le fasi: detect_band → tier → decompose → can_dispatch → quality_check → save/load pattern → calibrate → cleanup
- ✅ 35/35 checks al 100%

### Per Ogni Task (enforcement automatico)
- [ ] Tutti i requisiti implementati (no stub, pass, TODO)
- [ ] Edge cases coperti (vuoto, null, duplicato, errore, limite)
- [ ] Test presenti (almeno 1 per funzione)
- [ ] Error handling presente (try/except, status code, messaggio)
- [ ] Convenzioni del progetto rispettate

### Per Ogni Batch
- [ ] Tutti i subagenti hanno consegnato? (nessun silenzioso)
- [ ] Tutti i file dichiarati esistono? (verifica fisica)
- [ ] Test suite completa passa? (pytest -q)
- [ ] Nessun conflitto tra file modificati?
- [ ] Nessun codice orfano o duplicato?

### Per Il Sistema
- [ ] First-pass rate calcolato e salvato
- [ ] Qualità media documentata
- [ ] Pattern di decomposizione catturato
- [ ] Lesson salvate (se applicabile)
- [ ] Calibrazione aggiornata
- [ ] Il loop si è fermato perché goal raggiunto (non per timeout)

---

## Phase 10 — Skill Ecosystem Integration

L'prometheus-engine non lavora nel vuoto. Queste skill complementari vanno caricate e riferite durante il loop:

### Quando caricare quale skill

| Fase Loop | Skill da caricare | Perché |
|-----------|-------------------|--------|
| Phase 0.5 (Plan, Tier 3+) | `plan` | Scrive piano strutturato con file paths esatti e codice copy-pasteable |
| Phase 1 (Decompose, task con logica) | `test-driven-development` | Ogni task che produce codice deve seguire RED→GREEN→REFACTOR. Includi "scrivi test prima" nei quality criteria del subagente |
| Phase 3 (Streaming Gather, validazione) | `verification-strategies` | Quando non esiste test suite canonica o l'ambiente non può girare test (dep rotte, no framework). Verifica con curl, type checks, import checks |
| Phase 3 (post-batch, quality review) | `requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix. Da caricare dopo che un batch è completo ma prima del git push |
| Phase 7 (Failure Escalation, primo livello) | `systematic-debugging` | Quando un task non converge dopo 3 retry, carica per root-cause analysis invece di ritentare alla cieca |
| Phase 7 (Failure Escalation, secondo livello) | `post-mortem` | Se escalation continua dopo systematic-debugging, carica per post-mortem strutturato: 5 Whys root cause + regression test + memory feed |
| Post-batch (Tier 3+ completato) | `deploy-release` | Version bump SemVer, changelog, git tag, deploy + health check + rollback plan. Solo se l'utente vuole deployare |
| Post-deploy (bug nelle prime 30 min) | `post-mortem` | Analisi post-mortem del bug in produzione, regression test, memory feed per prevenzione futura |

### Come integrare nel loop

```
DURING DECOMPOSITION (Phase 1):
  └─ Per task che produce codice:
     └─ Quality criteria include: "Segui TDD: test prima, poi implementazione"
     └─ Subagente context include: "Carica skill test-driven-development"

DURING STREAMING GATHER (Phase 3):
  └─ Per validazione file:
     └─ Se test suite esiste: pytest -q (standard)
     └─ Se NON esiste o environment rotto: carica verification-strategies
        └─ Verifica con: import check, curl endpoint, type stub check, syntax check

AFTER BATCH COMPLETE, BEFORE GIT PUSH:
  └─ Carica requesting-code-review
     └─ Security scan sui file del batch
     └─ Quality gates (linting, type check)
     └─ Auto-fix se possibile, altrimenti retry nel loop

DURING ESCALATION (Phase 7) — LADDER A 2 LIVELLI:
  └─ Livello 1 (dopo 3 retry falliti):
     └─ Carica systematic-debugging
     └─ 4-phase root cause: understand → isolate → fix → verify
     └─ Se root cause trovata → retry con fix mirato (non escalare)
  └─ Livello 2 (se livello 1 non risolve):
     └─ Carica post-mortem
     └─ 5 Whys root cause + regression test + memory feed
     └─ Post-mortem leggero: salva lezione in memory, aggiungi test
     └─ Se ancora bloccato → escala all'utente con post-mortem documentato

POST-BATCH (Tier 3+ completato, tutti test passano):
  └─ Se utente vuole deployare:
     └─ Carica deploy-release
     └─ Pre-deploy checklist → version bump → changelog → tag → deploy
     └─ Health check post-deploy (OBBLIGATORIO)
     └─ Se health check fallisce → rollback + carica post-mortem
  └─ Se utente NON vuole deployare:
     └─ Solo commit + push finale (già fatto nel loop)

POST-DEPLOY MONITORING (primi 30 min):
  └─ Se bug emerge in finestra critica:
     └─ Carica post-mortem immediatamente
     └─ Post-mortem completo: timeline + 5 Whys + impact + action items
     └─ Memory feed: 2 entry (lezione specifica + pattern di classe)
     └─ Regression test aggiunto al codebase
```

### Pre-flight augmentation

Aggiungi al Pre-Flight Checklist (Phase 2c):
```
□ Task che producono codice hanno quality criteria TDD?
□ So quale skill di verification usire se pytest non disponibile?
□ Ho un piano di code review post-batch?
□ Ho fatto il recall dei pattern precedenti (Phase 4b)?
□ Se Tier 3+: il piano (Phase 0.5) è stato scritto e letto?
□ Se deploy previsto: pre-deploy checklist (deploy-release Phase 1) verificata?
□ ⚠️ HO VERIFICATO CHE IL NUMERO DI SUBAGENTI È PROPORZIONATO AL TIER?
   └─ NON dispatchare 100 subagenti per un Tier 2. Usa la tabella:
      T1→0, T2→1-5, T3→5-30, T4→30-100. Dinamico, mai fisso.
□ Se uso orchestrator: B1-B6 verificati? (mini-batch, depth, snapshot, retry, timeout, budget)
   └─ Vedi references/orchestrator-control.md per la Pre-Dispatch Checklist completa
```

---

## Phase 11 — Long Session Management

**Per sessioni di 2h+ con 30+ turni.** Il contesto cresce, la qualità degrada, le decisioni architetturali si dimenticano.

### Il Problema

```
Turno 1-10:  qualità 8/10 ✅
Turno 11-20: qualità 7/10 ⚠️ (context al 50%)
Turno 21-30: qualità 5/10 ❌ (context all'80%, compression death spiral)
```

### La Soluzione — 3 Meccanismi

Script reale: `scripts/session_manager.py` → classe `SessionManager`

#### 1. Session State File (su disco, non in context)

```python
from session_manager import SessionManager

sm = SessionManager("build_auth", "Implementa autenticazione JWT completa")
sm.track_turn(action="creato modello User", files=["models.py"], score=8)
sm.track_decision("Usare JWT refresh rotation", "Più sicuro per mobile")
```

Lo stato viene salvato su `~/.hermes/sessions/<id>_<turno>.json`.
NON tenere tutta la cronologia in context — solo un **context summary** di ~200 token.

#### 2. Checkpoint Automatico

```python
# Ogni 8 turni o 10 minuti
if sm.should_checkpoint():
    cp = sm.checkpoint()
    # comprime i turni passati, tiene solo ultimi 3 dettagliati
    # salva su disco, libera memoria
```

Il checkpoint produce un summary come questo:
```
=== SESSION STATE: build_auth ===
Goal: Implementa autenticazione JWT completa
Turni: 20 | Qualità: 7.7/10 (stable)
File: models.py, routes.py, auth.py, test_auth.py, middleware.py
Decisioni: Usare JWT refresh rotation (turno 5)
Ultimo checkpoint: turno 16
```

#### 3. Quality Trend Monitor

Rileva degradazione nelle ultime 5 valutazioni:

```python
# Se quality_trend == "degrading" → alert + rallenta
if sm.get_context_summary() contains "degrading":
    # Riduci complessità del prossimo task
    # Fai un checkpoint
    # Verifica decisioni architetturali
```

### Interrupt Recovery

Se la sessione si interrompe (crash, chiusura, cambio task):

```python
sm = SessionManager("build_auth", "Implementa autenticazione JWT completa")
recovery = sm.recover()
# recovery = {
#   "status": "recovered",
#   "total_turns": 20,
#   "files_created": ["models.py", "routes.py", ...],
#   "last_action": "fix typo",
#   "last_score": 8,
#   "suggestion": "Eri al turno 19: 'fix typo'. Prosegui con..."
# }

# Usa il context summary per riprendere senza perdere contesto
context = sm.get_context_summary()
```

### Context Summary (cosa mettere nel prompt invece della cronologia)

Quando il context è saturo (>60%), invece di ripetere tutta la cronologia, usa:

```
=== SESSION STATE: {session_id} ===
Goal: {goal}
Turni completati: {N}
Qualità media: {X}/10 ({trend})
File modificati: {file1}, {file2}, ...
Decisioni architetturali: {N}
  - [{turn}] {decisione}
Ultimo checkpoint: turno {turn}
⚠️ La qualità sta degradando — semplifica i prossimi task.
```

### Pre-Flight Augmentation (per Fase 2c)

Aggiungi al Pre-Flight Checklist:
```
□ Se sessione > 10 turni: SessionManager inizializzato?
□ Se context > 60%: checkpoint fatto + context summary usato?
□ Quality trend monitorato? (degrading → semplifica)
```

## Pitfalls (v4 Criticali)

### ❌ Il loop non è veramente autonomo
Se mi fermo a "pianificare" invece di decidere e agire, non sono un loop autonomo. Valuta stato → agisci → ripeti. Non "pianifica → pianifica ancora → agisci".

### ❌ Streaming gather dimenticato
Se aspetto TUTTI i risultati prima di ritentare, perdo il vantaggio dello streaming. I retry devono partire APPENA arriva un risultato sotto soglia.

### ❌ Decomposizione non adattiva
Se la decomposizione è sempre uguale, non sfrutto 100 subagenti. Deve scalare col numero di subagenti disponibili.

### ❌ Pattern di scala non usati
Avere 100 subagenti e usarne 10 è spreco. Se ho 100 slot, devo decomporre in 80-100 task.

### ❌ Self-learning saltato
La vera potenza è che migliora ogni volta. Se non salvo pattern, non calibro, non imparo. Il self-learning NON è opzionale.

### ❌ Quality threshold ignorato
Se accetto score 5/10 perché "tanto funziona", il loop non serve. La soglia è lì per un motivo.

### ❌ Escalation saltata
Se un task non converge e invece di escalare all'utente lo nascondo, il sistema produce qualità bassa.

### ❌ Non verificare i file fisici dei subagenti
I subagenti possono dichiarare "files_created: [a, b, c]" ma a e b non esistono. Verifica sempre con read_file + grep.

### ❌ FastAPI route ordering — route statiche DOPO `/{param}` (bug silenzioso)
In FastAPI, route statiche DOPO route dinamiche non vengono mai chiamate. Definisci SEMPRE tutte le route statiche PRIMA di `/{param}`.

### ❌ Python .pyc cache — modifiche ai .py ignorate
Dopo modifiche, elimina TUTTI i `__pycache__` e `.pyc`. Usa `python -B` per disabilitare.

### ❌ SQLite schema migration — `create_all` non altera tabelle esistenti
`Base.metadata.create_all(engine)` NON modifica tabelle esistenti. Migra manualmente con ALTER TABLE.

### ❌ Server old process zombie — codice nuovo ignorato
Quando modifichi il backend e riavvii, un vecchio processo può restare in ascolto sulla porta e servire codice vecchio. Il nuovo processo crasha con `[Errno 10048] address already in use`.

**Procedura di kill verificato:**
1. Trova il PID reale: `netstat -ano | grep :PORTA | grep LISTEN`
2. Kill: `taskkill -F -PID <PID>` (Windows) o `kill -9 <PID>` (Linux/Mac)
3. **VERIFICA** che la porta sia libera: `netstat -ano | grep :PORTA` → deve tornare vuoto
4. Se un altro processo riappare, ripeti dal passo 1 (zombie multipli possibili)
5. Avvia il server e verifica che serva codice FRESCO — non solo che risponda:
   `curl -s endpoint | python -c "import sys,json; d=json.load(sys.stdin); print('nuovo_campo' in d)"` — se il nuovo campo non c'è, il codice non è fresco

**Caso Windows (.pyc timestamps):** Su Windows i file `.pyc` possono avere timestamp più recenti dei `.py` (git checkout, filesystem caching). Python usa il `.pyc` senza ricompilare anche se il `.py` è stato modificato. Soluzione:
   - `find . -type d -name __pycache__ -exec rm -rf {} +`
   - Oppure usa `python -B` durante lo sviluppo per disabilitare la cache
   - In alternativa, avvia il server con `--reload` (uvicorn) che forza il refresh

### ❌ API response shape disallineata tra backend subagente e frontend subagente
Dopo batch paralleli backend+frontend, verifica che i campi che il frontend legge esistano nella response JSON dell'API.

### ❌ Function signature mismatch tra subagenti backend paralleli
Il caso più subdolo: subagente A produce `router.py` che chiama `build_prompt(...)`, subagente B produce `ollama_client.py` che definisce `build_prompt(...)`. Se le firme non combaciano (parametri diversi, uno usa `await` e l'altro no), il codice si rompe silenziosamente. **Soluzione:** il contratto interfaccia (Phase 1c) DEV'essere nel context di dispatch di entrambi i subagenti. Non basta dire "leggi il file X" — la firma esatta va copiata nel prompt di ogni subagente che la usa.

### ❌ External API keys non configurate ma fonte attiva
Se una fonte API è attiva (`source_foo=true`) ma la chiave non è configurata (`foo_key=""`), i fetcher ritornano `[]` silenziosamente. Questo può confondere il debugging perché sembra che l'API non risponda. **Soluzione:** logga un warning quando una fonte è attiva ma senza chiave, oppure disabilita la fonte di default.

### ❌ Ollama cloud model response wrapper non estratto correttamente

Quando chiami un modello Ollama (cloud o locale), la risposta HTTP è un wrapper `{"model":"...", "response":"...", "done":true,...}`. Il contenuto generato dal modello è nel campo **`response`**, non nell'intero JSON. Se passi `response.text` direttamente a `json.loads()`, ottieni il wrapper invece del JSON atteso.

**Soluzione:** estrai `payload.get("response")` prima del parsing. Vedi `references/ollama-integration.md` per il pattern completo (estrazione JSON, strategie di fallback, timeout, subscription check).

### ❌ Modelli cloud Ollama richiedono abbonamento

I modelli con tag `:cloud` (es. `glm-5.1:cloud`, `deepseek-v4-flash:cloud`) richiedono autenticazione (`ollama login`) e talvolta un abbonamento a pagamento. L'API ritorna 403 se non si è autorizzati. Prima di implementare, verifica con `curl -X POST http://localhost:11434/api/generate -d '{"model":"...","prompt":"test","stream":false}'` se il modello risponde.

### ❌ Confondere "autonomo" con "senza supervisione"
Autonomo = prendo decisioni da solo, ma DOCUMENTO tutto. Il final report non è opzionale.

### ❌ Autovalutazione troppo generosa — valuta l'esecuzione, non il design
Il self-feedback 0-100% alla fine di ogni task deve valutare **cosa è stato realmente eseguito e testato**, non quanto è bello il design sulla carta. Un sistema complesso (es. orchestrator a 4 livelli) che non è mai stato testato con subagenti reali non merita 90+/100, per quanto elegante sia l'architettura. Sii onesto: se una funzionalità è progettata ma non eseguita, abbassa il voto e segnala il gap nel "miglioramento".

### ❌ Saltare la clarification interview (Tier 3+)
Per Tier 3-4, partire direttamente con il plan senza fare domande all'utente = piano basato su assunzioni = retry inutili = spreco di token. 2 minuti di domande ben fatte risparmiano 20 minuti di retry. La clarification interview (Phase 0.5a) è **obbligatoria per Tier 3+** a meno che la richiesta non sia già completa di tutte le informazioni necessarie. Non fare domande una alla volta (fastidioso) — batch in un unico messaggio con default suggeriti.

### ❌ Self-learning senza guardrail — inquinamento skill e memory
Il self-learning è potente ma **pericoloso senza guardrail**. Rischi concreti:
- **Memory overflow**: 2200 char budget, entry infinite lo saturano → entry utili sovrascritte
- **Circular learning**: il modello impara dai propri errori e propaga lezioni sbagliate
- **Skill drift**: patch piccoli ma sbagliati si accumulano → la skill degrada silenziosamente
- **Skill proliferation**: 50 skill simili che si sovrappongono → context overload
- **Project contamination**: lezioni del progetto A contaminate il progetto B

**Soluzione:** i 10 guardrail in Phase 4f sono NON-OPZIONALI. Leggili, applicali, non saltarli. Il self-learning è autonomo nel DETECT (cosa imparare), ma collaborativo nel ACT (modifiche strutturali richiedono consenso umano).
### ❌ Spreco di subagenti — 100 per tutto

`max_concurrent_children: 100` è un **tetto massimo**, non un default. Dispatchare 100 subagenti per un task che ne richiede 3 è uno spreco di token e denaro (100× costo API). Il Tier system regola dinamicamente quanti subagenti usare:

- Tier 1 (0-1 file) → 0 subagenti, esegui direttamente
- Tier 2 (2-5 file) → 1-5 subagenti
- Tier 3 (5-20 file) → 5-30 subagenti
- Tier 4 (20-100+ file) → 30-100 subagenti

**Prima di dispatchare, chiediti SEMPRE: "Questo task ha davvero bisogno di N subagenti?"** Se la risposta è no, riduci. Il risparmio è cumulativo across sessioni.

### ❌ Orchestrator bottleneck — 6 Trappole Strutturali
L'architettura a 4 livelli (Parent→Orchestrator→Leaf→Micro-worker) ha 6 bottleneck identificati e risolti con regole B1-B6 in `references/orchestrator-control.md`:

1. **B1 Serializzazione**: `delegate_task` è bloccante → mini-batch da 5, non tutti insieme
2. **B2 Costo token**: 4 livelli = 4.5× costo → depth auto-limit basata su Tier
3. **B3 Perdita contesto**: micro-worker non sa il progetto → context snapshot <200 token
4. **B4 Retry amplification**: retry con micro-worker raddoppia costi → degradazione forzata inline
5. **B5 Timeout conflict**: finestra morta 360s → timeout allineati (60-120-240-300s)
6. **B6 Context overflow**: overflow silenzioso → `can_dispatch()` preventivo OBBLIGATORIO

**Verifica sempre la Pre-Dispatch Checklist** in `references/orchestrator-control.md` prima di ogni batch con orchestrator.

### ❌ Subagenti su codebase familiare — overhead inutile

La tabella Dynamic Allocation assume codebase sconosciuto. Se **conosci già il progetto** (esplorato in sessioni precedenti), applicare 5-30 subagenti per un Tier 3 è puro overhead:
- Ogni subagente deve leggere i file per capire la struttura — tu già la conosci
- Ogni subagente produce un summary che satura il context — tu non hai bisogno di quei summary
- Il dispatch + attesa + validazione richiede più tempo dell'esecuzione diretta

**Soluzione:** usa il Fattore Familiarità (sezione Dynamic Subagent Allocation). Se hai già letto/scritto il codebase, riduci i subagenti a 0 ed esegui direttamente. Verifica con import check + test live (stessa qualità, 10× più veloce).

### ❌ Context window overflow — 100 summary saturano il parent
Dispatchare 100 subagenti significa ricevere 100 summary nel context del parent. Anche con `max_summary_chars: 24000`, 100 × 2000 token = 200K token di summary che si aggiungono al context esistente. **Questo può saturare la context window e causare compression death spiral** (comprime → perde context → retry duplica task → altri summary → overflow → crash).

**Soluzione (Phase 3e):** dispatch a ondate (max 20-25 subagenti simultanei per Tier 3+), summary compression proattiva (istruisci subagenti a summary concisi), e monitora i trigger di compression (2+ trigger = riduci batch size).

### ❌ Band filter tie-breaking — sovrastima preferibile a sottostima
Il `detect_band()` in `scripts/prometheus_engine.py` usa tie-breaking che preferisce la banda più alta in caso di pareggio. Questo è intenzionale: è meglio caricare la skill per un task "media" che scoprire a metà che era "alta". Tuttavia, il filtro può classificare "aggiungi validazione email al form" come `media` invece di `bassa` perché "validazione" è una parola strutturale. Questo è **accettabile** — la validazione è una modifica strutturata, non un typo. Non cercare di "fixare" il filtro per catturare più task in `bassa` — il rischio è sottostimare un task reale e saltare il loop quando serviva.
