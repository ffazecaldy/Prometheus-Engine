---
tags: [prometheus-engine, filosofia, core-loop]
aliases: [Filosofia, Core Loop, Philosophy]
---

# Filosofia e Core Loop

**"I don't follow a workflow. I AM the loop."**

Il Prometheus Engine è un sistema agentico autonomo che:

1. **Decide cosa fare** — basato sullo stato corrente, non un piano fisso
2. **Esegue in parallelo** — fino a 100 subagenti per batch, SOLO quando serve
3. **Valuta e ritenta** — streaming gather, nessun ritardo batch
4. **Impara e si adatta** — salva pattern, migliora ogni iterazione
5. **Continua fino a completamento** — zero intervento umano

## Il Core Loop

```
while goal_not_achieved:
    state = assess_progress(goal, completed, gaps)
    if state.is_done: break
    tasks = decompose_remaining(state.gaps, state.optimal_scale)
    dispatch_all(tasks)
    for each_result in stream():
        if result.passed: continue
        dispatch_retry(result)
    update_metrics(state)
```

## Collegamenti
- [[Tier System]] — Determina la scala del loop
- [[Fase 0 - Autonomous Loop Engine]] — Initialize State → Assess → Decide
- [[Pitfalls]] — ❌ Il loop non è veramente autonomo
- [[Configurazione]] — Prerequisiti per far girare il loop
