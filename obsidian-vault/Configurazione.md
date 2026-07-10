---
tags: [prometheus-engine, configurazione, setup]
---

# Configurazione

## Config YAML Necessari

```bash
hermes config set delegation.max_concurrent_children 100
hermes config set delegation.max_spawn_depth 3    # 4 livelli: Parent→Orch→Leaf→Micro
hermes config set delegation.max_iterations 100
hermes config set delegation.child_timeout_seconds 300  # B5: allineato con cascade 4 livelli
hermes config set delegation.subagent_auto_approve true
hermes config set agent.max_turns 120
hermes config set approvals.mode smart
hermes config set code_execution.max_tool_calls 100
hermes config set compression.protect_first_n 5
```

**Importante:** le modifiche richiedono una **nuova sessione** (`/reset` o riavvio Hermes).

## Verifica

```bash
grep -E "max_concurrent_children|max_spawn_depth|max_turns|approvals" ~/.hermes/config.yaml
```

## Toolset Richiesti
- terminal (git, python, uv)
- file (read, search, write, patch)
- web (search, fetch)
- delegation (subagenti)
- cron (auto-verify)

## Collegamenti
- [[Filosofia e Core Loop]] — Il loop che questa config abilita
- [[Tier System]] — 100 subagenti = tetto massimo
- [[Pitfalls]] — ❌ Modelli cloud Ollama
