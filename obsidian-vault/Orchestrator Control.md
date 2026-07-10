---
tags: [prometheus-engine, orchestrator, multi-level, delegation, dynamic-split, bottleneck]
aliases: [Controllo Sub-agenti, Orchestrator Control, Leaf Split, Anti-Bottleneck]
---

# Orchestrator Control — Controllo Sub-Agenti Dinamico

Gestione di orchestratori, leaf e micro-worker per task corposi. 6 regole anti-bottleneck integrate.

## Architettura a 4 Livelli

```mermaid
graph TD
    P[PARENT<br/>Prometheus Engine<br/>Livello 0] --> O1[ORCHESTRATOR Backend<br/>max 8 worker/batch]
    P --> O2[ORCHESTRATOR Frontend<br/>max 5 worker/batch]
    P --> O3[ORCHESTRATOR Test<br/>max 5 worker/batch]

    O1 --> L1[LEAF: models/user.py]
    O1 --> L2[LEAF: routes/auth.py]
    O1 --> L3[LEAF: services/auth.py]

    O2 --> L4[LEAF: Login component]
    O2 --> L5[LEAF: Dashboard component]

    O3 --> L6[LEAF: test_auth.py]
    O3 --> L7[LEAF: test_models.py]

    L2 -.->|B2: depth OK<br/>B6: budget OK| MW1[MICRO-WORKER 1<br/>JWT encode]
    L2 -.->|split dinamico| MW2[MICRO-WORKER 2<br/>JWT decode]

    L7 -.->|task complesso| MW3[MICRO-WORKER 1<br/>test edge cases]
    L7 -.->|split dinamico| MW4[MICRO-WORKER 2<br/>test happy path]

    style P fill:#1e3a5f,color:#fff
    style O1 fill:#2d6a4f,color:#fff
    style O2 fill:#2d6a4f,color:#fff
    style O3 fill:#2d6a4f,color:#fff
    style L1 fill:#52796f,color:#fff
    style L2 fill:#52796f,color:#fff
    style L3 fill:#52796f,color:#fff
    style L4 fill:#52796f,color:#fff
    style L5 fill:#52796f,color:#fff
    style L6 fill:#52796f,color:#fff
    style L7 fill:#52796f,color:#fff
    style MW1 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
    style MW2 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
    style MW3 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
    style MW4 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
```

## 🛡️ 6 Regole Anti-Bottleneck

### B1 — Mini-Batch Streaming
Orchestrator dispatcha in **batch da 3-5 leaf**, non tutti insieme. Riduce la finestra di attesa se un leaf è lento.

### B2 — Depth Auto-Limit
La profondità massima dipende dal Tier, non è fissa:

| Tier | Familiarità | Depth max | Micro-worker? |
|------|-------------|-----------|---------------|
| 1-2 | qualsiasi | 0-1 | Mai |
| 3 | bassa | 2 | Mai |
| 3 | alta | 1 | Mai |
| 4 | bassa | 3 | Solo se >50 file |
| 4 | alta | 2 | Solo se 1 leaf anomalo |

### B3 — Context Injection Compatto
Ogni subagente riceve un **context snapshot < 200 token** con progetto, stack, convenzioni, goal globale.

### B4 — Retry Without Micro-Worker
Ogni retry **rimuove un livello di delega**:
- Tentativo 1: leaf + micro-worker
- Tentativo 2: leaf inline (0 micro-worker)
- Tentativo 3: orchestrator inline (0 leaf)

### B5 — Timeout Allineati
```bash
hermes config set delegation.child_timeout_seconds 300  # era 600
```

| Livello | Timeout | Margine |
|---------|---------|---------|
| Micro-worker | 60s | — |
| Leaf | 120s | 60s dopo micro |
| Orchestrator | 240s | 120s dopo leaf |
| Parent | 300s | 60s dopo orch |

Finestra morta: **0 secondi**.

### B6 — Context Budget Enforcement
Calcolo preventivo **OBBLIGATORIO** prima di dispatch. Se overflow:
1. Micro-worker → 0
2. Leaf: 8 → 5 per orchestrator
3. Orchestrator: 4 → 2
4. Tutto inline

## 🔄 Leaf Dynamic Split

```mermaid
flowchart TD
    Start[Leaf riceve task] --> B2{B2: Depth OK?}
    B2 -->|No| Exec[Esegui direttamente]
    B2 -->|Sì| B6{B6: Budget OK?}
    B6 -->|No| Exec
    B6 -->|Sì| Eval{Valuta complessità}
    Eval -->|1 file, <30s| Exec
    Eval -->|2-3 file semplici| Exec
    Eval -->|3+ file con dipendenze<br/>stime >120s| Split[Split in 2 sub-task]

    Split --> MW1[Micro-worker 1<br/>+ context snapshot B3]
    Split --> MW2[Micro-worker 2<br/>+ context snapshot B3]

    MW1 --> R1{Risultato}
    MW2 --> R2{Risultato}

    R1 -->|Pass| Merge[Leaf unisce risultati]
    R2 -->|Pass| Merge
    R1 -->|Fail| B4A[B4: retry 1x<br/>poi inline]
    R2 -->|Fail| B4B[B4: retry 1x<br/>poi inline]

    Merge --> Done[Restituisce all'orchestrator]
    Exec --> Done

    style Start fill:#52796f,color:#fff
    style B2 fill:#9d4e15,color:#fff
    style B6 fill:#9d4e15,color:#fff
    style Eval fill:#1e3a5f,color:#fff
    style Split fill:#9d4e15,color:#fff
    style Merge fill:#2d6a4f,color:#fff
    style Done fill:#1e3a5f,color:#fff
    style MW1 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
    style MW2 fill:#cad2c5,color:#000,stroke-dasharray: 5 5
    style B4A fill:#f97316,color:#fff
    style B4B fill:#f97316,color:#fff
```

### Guardrail Leaf Split
- MAX 2 micro-worker (hard limit)
- Micro-worker = dead-end
- B2: depth check per Tier
- B3: context snapshot < 200 token
- B4: degradazione forzata nei retry
- B5: timeout 60s → leaf inline
- B6: budget check prima di spawnare

## Configurazione

```bash
hermes config set delegation.max_spawn_depth 3    # 4 livelli
hermes config set delegation.max_concurrent_children 100
hermes config set delegation.child_timeout_seconds 300  # B5 allineato
```

## Pre-Dispatch Checklist

```
□ B1: Mini-batch da max 5 leaf?
□ B2: Depth appropriata per Tier?
□ B3: Context snapshot < 200 token?
□ B4: Strategia retry con degradazione?
□ B5: child_timeout = 300?
□ B6: can_dispatch() verificato?
□ Familiarità codebase valutata?
```

## Collegamenti
- [[Fase 2 - Autonomous Scatter]] — Dispatch base
- [[Fase 5 - Scale Patterns]] — Pattern per 100 subagenti
- [[Fase 3 - Streaming Quality Gate]] — Validazione
- [[Fase 7 - Failure Escalation]] — Error propagation
- [[Configurazione]] — max_spawn_depth=3, child_timeout=300
- [[Guardrail]] — I 10 guardrail self-learning
- [[Pitfalls]] — ❌ Context window overflow
