---
tags: [prometheus-engine, fase-3d-ter, security, regex]
---

# Phase 3d-ter — Security Shield AUTO

Check di sicurezza **verificabile automaticamente via regex**. Applicabile a TUTTI i task di codice, anche Tier 1. Se fallisce → retry immediato.

## 1. Zero Hardcoded Secrets (CRITICO — blocca)

```
Regex: \b(api_key|password|secret|token|api_secret)\s*=\s*['\"][^'\"]{8,}
       SENZA os.getenv / env / process.env nelle 3 righe successive

❌ API_KEY = 'sk-abc123...'
❌ password = 'admin'
✅ API_KEY = os.getenv('API_KEY')
✅ password = get_secret()
```

Se trovato → ❌ RETRY: "Sposta la credenziale in variabile d'ambiente"

## 2. SQL Injection Risk (ALTO — blocca)

```
Regex: f-string SQL, .format() SQL, concatenazione + SQL

❌ f"SELECT * FROM users WHERE id={user_id}"
❌ "SELECT * FROM " + table_name
✅ cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
✅ session.query(User).filter(User.id == user_id)  [ORM]
```

Se trovato → ❌ RETRY: "Usa query parametrizzate o ORM, mai f-string SQL"

## 3. Placeholder Secrets (Warning — non blocca)

```
Regex: \b(API_KEY|TOKEN|SECRET)\s*=\s*(['\"]\s*['\"]|None|''|\"\")\s*#\s*TODO

⚠️ API_KEY = ''  # TODO: add key
```

Se trovato → ⚠️ WARNING nel log (non blocca, potrebbe essere intenzionale)

## Implementazione

Le regex sono eseguite da `quality_check()` in `scripts/prometheus_engine.py` come **Check 5**, dopo il syntax check e prima del quality gate.

## Collegamenti

- [[Fase 3 - Streaming Quality Gate]] — Dove si inserisce nella pipeline
- [[Guardrail 11 - Security Shield]] — Il guardrail che formalizza queste regole
- [[Quality Check]] — Il modulo che esegue il check
- [[Phase 1d-bis - Clean Code Standards]] — Check complementare di qualità codice
