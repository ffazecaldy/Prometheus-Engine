---
tags: [prometheus-engine, pattern, weather, meteo]
---

# Weather API Integration

Pattern specifico per progetti meteo.

## Multi-Source Fetcher
- Open-Meteo (gratuito, 7 modelli)
- NWS/NOAA (USA)
- Meteoblue (API key)
- OpenWeatherMap, WeatherAPI, Tomorrow.io
- Visual Crossing, Weatherbit, AccuWeather

## Caratteristiche
- Temperature arrotondate a 1 decimale
- Ogni fonte ha timeout separato
- Errori isolati per fonte
- Aggregatore `fetch_all_sources()` chiama tutte le fonti in sequenza

## Collegamenti
- [[External API Integration]] — Pattern generale
- [[Climatology 3 Levels]] — Analisi storica
- [[Ollama Integration]] — AI analizza i dati raccolti
