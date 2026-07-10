---
tags: [prometheus-engine, pattern, api, external]
---

# External API Integration

Pattern per integrare API esterne multiple.

## Design Pattern
- Flag booleano `source_foo` per attivare/disattivare
- Chiave API da `.env`
- Timeout configurabile per fonte
- Errore di una fonte NON blocca le altre
- Ogni fonte ritorna `SourceForecast` con `error` opzionale

## Esempio (weather_sources.py)
```python
async def fetch_all_sources(lat, lon, target_date, country_code):
    sources = []
    sources.extend(await fetch_open_meteo(lat, lon, target_date))
    if country_code == "US":
        sources.extend(await fetch_nws(lat, lon, target_date))
    sources.extend(await fetch_meteoblue(lat, lon, target_date))
    # ... altre fonti
    return sources
```

## Collegamenti
- [[Weather API Integration]] — Pattern specifico meteo
- [[Ollama Integration]] — Pattern specifico AI
- [[Fase 1 - Massive Decomposition]] — Interface contracts per API
