# External API Integration Pattern

When implementing multiple external APIs (weather, data, AI, etc.) as parallel sources in a Python project, use this pattern to keep each source isolated, configurable, and resilient.

## Structure

```
app/
  config.py            # Pydantic Settings: one flag + one key field per API
  weather_sources.py   # One async function per source, all returning same type
  router.py            # Aggregator calls all enabled sources
```

## Per-source function template

```python
SOURCE_NAME_URL = "https://api.example.com/v1/endpoint"
SOURCE_NAME_MAX_DAYS = 7          # forecast horizon

async def fetch_sourcename(lat: float, lon: float, target_date: date) -> list[SourceForecast]:
    # 1. Guard: check feature flag + API key
    if not settings.source_sourcename or not settings.sourcename_key:
        return []

    # 2. Guard: horizon check (future + past)
    days_ahead = (target_date - date.today()).days
    if days_ahead > SOURCE_NAME_MAX_DAYS or days_ahead < 0:
        return []

    # 3. HTTP call with try/except
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(SOURCE_NAME_URL, params={...}, timeout=15)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        return [SourceForecast(source="sourcename", model_name="SourceName",
                               max_temp_c=None, forecast_date=target_date,
                               retrieval_date=datetime.now(timezone.utc),
                               days_until_target=days_ahead, error=str(exc))]

    # 4. Extract value, return single-element list
    value = extract_temp_from_response(data, target_date)
    return [SourceForecast(source="sourcename", model_name="SourceName",
                           max_temp_c=round(value) if value is not None else None,
                           forecast_date=target_date,
                           retrieval_date=datetime.now(timezone.utc),
                           days_until_target=days_ahead)]
```

## Config pattern

```python
class Settings(BaseSettings):
    source_sourcename: bool = False    # off by default
    sourcename_key: str = ""           # empty by default
```

## API key handling

- **Backend**: read from `.env` via Pydantic Settings
- **Frontend**: stored in `localStorage`, displayed with `type="password"` + eye reveal toggle
- **Security**: `.env` files are blocked by `read_file` to prevent credential leakage
- **No-key = silent skip**: each fetcher returns `[]` when disabled, not an error

## Aggregator

```python
async def fetch_all_sources(lat, lon, target_date, country_code=""):
    sources = []
    sources.extend(await fetch_open_meteo(lat, lon, target_date))
    sources.extend(await fetch_nws(lat, lon, target_date))
    sources.extend(await fetch_sourcename(lat, lon, target_date))
    return sources
```

## Adding a new source (checklist)

1. Add `source_<name>: bool = False` + `<name>_key: str = ""` to `config.py`
2. Create `async def fetch_<name>(lat, lon, target_date) -> list[SourceForecast]` in sources module
3. Add call to `fetch_all_sources()`
4. Add to `.env.example`
5. Add UI toggle + key input in `SettingsPanel.jsx`
6. Verify: no-key → `[]`, past date → `[]`, beyond horizon → `[]`, real call → valid data

## Rounding

User prefers **integer temperatures** (33°C not 33.4°C). Apply `round()` in every fetcher before creating `SourceForecast`:

```python
value = round(value)  # float → int
```

Also round climatology metrics (`mean`, `std`, etc.) and ensure the Ollama prompt says *"solo numeri interi"*.

## Vendor-specific patterns

### Meteoblue

**⚠️ Package `basic-1d` è deprecato. Usa `basic-1h`.**

- Endpoint: `https://my.meteoblue.com/packages/basic-1h`
- Params: `apikey`, `lat`, `lon`, `asl=0`, `format=json`, `forecast_days`
- Response: `data_1h.temperature[]` + `data_1h.time[]` — array orari
- Calcola la max giornaliera aggregando i dati delle 24 ore per la data target:
  ```python
  times = data["data_1h"]["time"]
  temps = data["data_1h"]["temperature"]
  day_temps = [t for t_str, t in zip(times, temps)
               if t is not None and t_str.startswith(target_str)]
  value = max(day_temps) if day_temps else None
  ```
- `forecast_days` minimo 3 (se chiedi meno, restituisce comunque 3+)
- Orizzonte: 7 giorni. Free tier: 1000/giorno. Richiede API key da meteoblue.com.

### AccuWeather (multi-step)

1. Location key: `GET /locations/v1/cities/geoposition/search?q={lat},{lon}&apikey={key}`
2. Forecast: `GET /forecasts/v1/daily/5day/{locationKey}?apikey={key}&metric=true`
- Free: 50/giorno, 5 giorni

### NWS/NOAA

- `GET /points/{lat},{lon}` → `gridId`, `gridX`, `gridY` → `GET /gridpoints/{gridId}/{gridX},{gridY}/forecast`
- Richiede `User-Agent` header. Temperature in °F → convert: `(temp_f - 32) * 5 / 9`
- Solo USA (lat 18–72, lon −60–−180). Orizzonte: 7 giorni.

### Open-Meteo Multi-Model

7 modelli indipendenti interrogati come richieste HTTP separate:
`gfs_global` (GFS), `ecmwf_ifs04` (ECMWF), `icon_global` (ICON), `gem_global` (GEM), `meteofrance_arpege_world` (MF-ARPEGE), `jma_gsm` (JMA-GSM), `bom_access_global` (BOM-Access)

> ⚠️ `meteoblue_nmm` (MeteoBlue-NMM) è stato **deprecato** dall'API Open-Meteo. Non usarlo.

- `https://api.open-meteo.com/v1/forecast`. Gratuito, no API key. Orizzonte: 16 giorni.
- Ogni modello va interrogato separatamente (parametro `models`). Se non copre una località: `null`.

## Pitfalls

- **Rate limits**: ogni API ha limiti free-tier diversi.
- **API key rotation**: chiave invalida → `SourceForecast(error=...)`, non crash.
- **Multi-step APIs**: AccuWeather richiede location key + forecast — entrambi gli step con error handling.
- **Temperature units**: NWS in °F → convertire.
- **Missing models**: Open-Meteo ritorna `null` per modelli che non coprono una località.
- **Timezone**: sempre `units=metric`, `timezone=UTC`.
- **Windows pipe crash**: su Windows git-bash, `curl ... | python -c "json.loads(...)"` può fallire silenziosamente. Usa sempre `curl ... -o file.json && python -c "json.load(open('file.json'))"` in contesti Windows.
