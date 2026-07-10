---
tags: [prometheus-engine, quality, enforcement, phase-9]
---

# Quality Check — Enforcement Automatico Phase 9

Implementazione reale: `scripts/prometheus_engine.py` → `quality_check()`

## Cosa Verifica

| Check | Descrizione | Metodo |
|-------|-------------|--------|
| **exists** | File esiste su disco | `os.path.exists()` |
| **not_empty** | File non è vuoto | `os.path.getsize() > 0` |
| **no_stub** | Nessun TODO/pass/stub | Regex `\b(TODO\|FIXME\|pass\|\\.\\.\\.)\b` |
| **syntax** | Sintassi Python valida | `compile(source, path, 'exec')` |

## Esempio

```python
from prometheus_engine import quality_check

result = quality_check(
    files_created=["app/routes.py", "app/models.py"],
    task_type="api",
    check_imports=True,
    check_stub=True,
    check_syntax=True,
)
# result = {
#   "passed": True,
#   "checks": [{"file": "...", "check": "exists", "passed": True}, ...],
#   "failures": [],
#   "total_files": 2,
#   "total_checks": 8,
# }
```

## Integrazione nel Loop

Dopo ogni task completato:
```python
if not quality_check(files_created)["passed"]:
    dispatch_retry(task_id, feedback="Quality check fallito: [...]")
```

## Collegamenti
- [[E2E Integration Test]] — Testato in tutti gli scenari
- [[Fase 3 - Streaming Quality Gate]] — Dove viene chiamato
- `scripts/prometheus_engine.py` — Implementazione
