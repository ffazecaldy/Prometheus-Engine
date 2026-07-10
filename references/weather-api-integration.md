# Pattern Integrazione API Meteo (Multi-Source)

## Architettura

Ogni fonte meteo è una funzione `async fetch_*(lat, lon, target_date) -> list[SourceForecast]` in `weather_sources.py`. L'aggregatore `fetch_all_sources()` le chiama tutte.

## Regole

1. **Temperature sempre intere**: usare helper `_int()` che fa `round(value) if value is not None else None`
2. **Orizzonte**: ogni fetcher controlla `days_ahead > MAX_DAYS` e ritorna `[]` se oltre
3. **Date passate**: ritornare `[]` (non chiamare API storiche)
4. **Errori resilienti**: wrap `try/except` — mai bloccare una fonte se un'altra fallisce
5. **Api key**: leggere da `settings.*_key`, default vuoto. Se fonte attiva ma chiave vuota → `[]`

## Aggiungere una nuova fonte

```python
# 1. Config
source_miafonte: bool = False
miafonte_key: str = ""

# 2. Fetcher in weather_sources.py
async def fetch_miafonte(lat, lon, target_date) -> list[SourceForecast]:
    if not settings.source_miafonte or not settings.miafonte_key:
        return []
    ...  # chiamata API, parsificazione
    return [SourceForecast(source="miafonte", model_name="MiaFonte", max_temp_c=_int(value), ...)]

# 3. Aggiungere a fetch_all_sources()
sources.extend(await fetch_miafonte(lat, lon, target_date))

# 4. SettingsPanel: aggiungere a API_SOURCES array
```

## Prompt AI arricchito

Prima di chiamare Ollama, il backend può fare una ricerca web (DuckDuckGo) per contesto meteo aggiuntivo. I risultati vanno passati come parametro `web_results` a `build_prompt()`. Il template del prompt include una sezione `## Ricerca web esterna`.

## Meteoblue API (caso specifico)

- Endpoint: `https://my.meteoblue.com/packages/basic-1h` (NON basic-1d, deprecato)
- Calcolare max giornaliero da dati orari: `max(temperature[t] per time[t] che inizia con target_date)`
- Parametri: `apikey`, `lat`, `lon`, `asl=0`, `format=json`, `forecast_days`
