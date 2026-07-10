# Benchmark Harness Pattern — Skill Hermes Agent

## Cosa

Pattern per costruire un harness di benchmark che testa una skill Hermes Agent
in modo ripetibile, confrontando più condizioni (baseline vs skill v1 vs v2),
con ground truth oggettiva (verify_cmd shell) e metriche aggregate in SQLite.

## Quando usarlo

- Vuoi sapere se una skill (o una nuova versione) migliora oggettivamente la qualità
- Devi confrontare più versioni della stessa skill o baseline vs skill attiva
- Hai bisogno di metriche quantitative (FPR, qualità, durata, token) per decidere
  se mergiare una modifica

## Architettura

```
bench-repo/
├── benchmark_harness.py       # Orchestratore
├── benchmark-schema.sql       # Schema SQLite (goals + runs + summary view)
├── goals.example.csv          # Task suite in CSV
├── bench.sqlite3              # (gitignored) DB dei run
└── skill-under-test/          # Skill da testare (clone/tag)
```

## Invocazione Hermes (verificata)

```bash
hermes --yolo --skills <skill_name> -z "<goal_text>" send
```

- `--yolo`: skip conferme interattive
- `--skills <name>`: attiva la skill; ometti per la condizione baseline
- `-z "<prompt>"`: one-shot mode — stampa output finale su stdout e ritorna
- `send`: esegue in modalità one-shot e ritorna il controllo

## Schema SQLite

```sql
CREATE TABLE benchmark_goals (
    goal_key TEXT PRIMARY KEY,
    goal_text TEXT NOT NULL,
    tier INTEGER CHECK(tier BETWEEN 1 AND 4),
    goal_type TEXT DEFAULT 'generic',
    verify_cmd TEXT NOT NULL,
    verify_description TEXT DEFAULT ''
);

CREATE TABLE benchmark_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_key TEXT REFERENCES benchmark_goals(goal_key),
    condition TEXT CHECK(condition IN ('baseline','skill-v1','skill-v2','skill-custom')),
    run_number INTEGER,
    verify_passed INTEGER,
    first_pass_rate REAL,
    avg_quality REAL,
    convergence_iterations INTEGER,
    silent_failures INTEGER,
    escalated INTEGER,
    duration_seconds REAL,
    total_tokens INTEGER,
    total_tool_calls INTEGER,
    parse_warnings TEXT,
    raw_output TEXT
);

CREATE VIEW benchmark_summary AS
SELECT goal_key, condition,
  AVG(verify_passed) AS verify_pass_rate,
  AVG(first_pass_rate) AS avg_first_pass_rate,
  AVG(avg_quality) AS avg_quality_score,
  AVG(duration_seconds) AS avg_duration_seconds,
  AVG(total_tokens) AS avg_total_tokens
FROM benchmark_runs GROUP BY goal_key, condition;
```

## Isolare il parser del report Hermes

La funzione `parse_hermes_report(raw_output)` deve essere:
- **Una sola funzione**, chiaramente marcata come da sostituire
- **Mai crashare**: se il parsing fallisce, ritorna valori di default + warning
- **Espandibile**: pattern regex facilmente aggiungibili

```python
def parse_hermes_report(raw_output: str) -> dict:
    """
    >>> SEZIONE DA MODIFICARE — calibra i regex sul tuo Hermes <<<
    """
    result = {"first_pass_rate": None, "avg_quality": None, ...}
    if not raw_output: return result
    # Pattern da adattare
    val = _try_extract(r"(?:\bfirst.?pass\b)\s*[:=]?\s*(\d+\.?\d*)%?")
    val = _try_extract(r"(?:qualit[àa]|avg...quality)\s*[:=]?\s*(\d+\.?\d*)\s*/?\s*10")
    return result
```

Avere una gemella `parse_hermes_report_json()` da attivare se Hermes
supporta `--json` è una precauzione a costo zero.

## Pitfall noti

### ❌ CSV delimiter + Python verify_cmd
I campi `verify_cmd` contengono codice Python con `;` (es. `import http.client; conn = ...`).
Usare `;` come delimiter CSV rompe tutto. **Soluzione:** genera il CSV con
`csv.writer(f, delimiter=';')` di Python che quota automaticamente i campi.
Mai scrivere a mano un CSV con verify_cmd complessi.

### ❌ verify_cmd con shell=True
`verify_cmd` spesso usa pipe e redirect (`2>&1`, `findstr`). Serve `shell=True` in
`subprocess.run()`. Accettabile perché il comando viene dal CSV che l'utente controlla,
ma da tenere a mente per sicurezza.

### ❌ Encoding Windows (cp1252 vs utf-8)
Su Windows, subprocess può restituire output in cp1252. Usa sempre:
`subprocess.run(..., encoding="utf-8", errors="replace")`

### ❌ Output Hermes enorme
L'output di `hermes -z` può essere lungo. Tronca a ~10K caratteri prima di salvarlo
nel DB, con marcatore `[TRONCATO]`.

### ❌ Timeout Hermes
Hermes può bloccarsi se il modello non risponde. Imposta `subprocess.TimeoutExpired`
con un timeout ragionevole (default 300s) e logga l'evento senza bloccare la suite.
