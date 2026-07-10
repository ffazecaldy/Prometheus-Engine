# Int → Float Precision for Polymarket Betting

## Quando serve

L'utente scommette su **Polymarket** per temperature massime giornaliere. I mercati Polymarket risolvono **al decimo di grado** (es. 34.3°C, non 34°C). L'app deve quindi supportare float con 1 decimale in tutto lo stack.

## Pattern di conversione

```
Schemas (Pydantic)     int → float
Database (SQLAlchemy)  Integer → Float  
Weather sources        round(x) → round(x, 1)
Climatology            round(x) → round(x, 1)
Prompt AI              "temperature intere" → "1 decimale"
Frontend               Math.round(x) → x.toFixed(1)
Router ensemble        round(mean) → round(mean, 1)
```

## File da modificare (ordine)

1. **schemas.py** — tutti i campi `Optional[int]` temperatura → `Optional[float]`. `expected_max_temp_c: int` → `float`
2. **models.py** — `Column(Integer)` → `Column(Float)` per temperature in `ForecastHistory` e `OllamaResponseCache`
3. **weather_sources.py** — `_int()` → `_float()` con `round(x, 1)`. Sostituire tutte le chiamate `_int(` con `_float(`
4. **climatology.py** — `round(mean)` → `round(mean, 1)`, idem per median, p10, p90, record
5. **ollama_client.py** — prompt: "TEMPERATURE CON 1 DECIMALE" invece di "TEMPERATURE INTERE". Range fasce: `"32.5-33.4°C"` invece di `"30-32°C"`. Esempio JSON: `34.3` invece di `34`
6. **router.py** — `_ensemble_stats`: `round(mean, 1)`. Fallback source: `round(..., 1)`. `climatology_match`: `round(max(0, 100 - diff * 8), 1)` per evitare floating point drift (`86.39999999999998%`)
7. **frontend/ResultView.jsx** — `Math.round(temp)` → `temp.toFixed(1)`. `Math.round(clim)` → `clim.toFixed(1)`

## Pitfall: Floating point drift

Quando fai `max(0, 100 - diff * 8)` con float, Python produce `86.39999999999998%` invece di `86.4%`.

**Fix:** avvolgi sempre con `round(..., 1)`:
```python
climatology_match = round(max(0, 100 - diff * 8), 1)
```

## Pitfall: Cache vecchie

Dopo aver cambiato i tipi in schemas/models, elimina `__pycache__` prima di riavviare:
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```
Altrimenti il server carica i `.pyc` vecchi e usa ancora `Optional[int]`.

## Verifica

```python
d = await post_forecast("Roma", "2026-07-11")
assert isinstance(d["ai_forecast"]["expected_max_temp_c"], float)
assert isinstance(d["climatology"]["mean_max_temp_c"], float)
assert isinstance(d["sources"][0]["max_temp_c"], float)
```
