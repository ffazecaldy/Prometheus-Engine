# Climatologia a 3 Livelli — Pattern per Previsioni Meteo AI

## Problema

La climatologia tradizionale analizza un singolo giorno su N anni (es. 10 Luglio × 10 anni = ~10 campioni).
Pochi campioni → statistica fragile, AI poco informata, confidenza poco affidabile.

## Soluzione

Una **singola chiamata API** all'archivio storico con range `[inizio_mese, fine_mese]` su 10 anni, poi 3 filtri:
```
API call: 2016-07-01 → 2025-07-31 (3318 dati grezzi, singola request HTTP)
  ├─ Filtro giorno esatto     → ~10 campioni  (media, std, mediana, trend, anomalia)
  ├─ Filtro ±5gg              → ~100 campioni (media, std, range)
  └─ Filtro mese intero       → ~310 campioni (media, std, record mese)
```

## Vantaggi

| Aspetto | 1 livello (solo giorno) | 3 livelli |
|---------|------------------------|-----------|
| Campioni | ~10 | ~310 (+3000%) |
| Robustezza statistica | Bassa (ogni anno anomalo pesa 10%) | Alta (ogni anno anomalo pesa ~0.3%) |
| Confidenza AI | Autovalutazione del modello | 3 scale temporali allineate |
| Record | Solo del giorno | Giorno + mese intero |
| Dati per trend | 10 punti | 310 punti (stessa API call) |

## Implementazione (FastAPI + Open-Meteo)

```python
# Fetch unico per tutto il mese
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
start_date = date(start_year, target_date.month, 1)
end_date = date(end_year, target_date.month, last_day)

params = {
    "latitude": lat, "longitude": lon,
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "daily": "temperature_2m_max",
    "timezone": "UTC",
}

# Indicizza: {(year, month, day): temp}
idx = {}
for time_str, temp in zip(times, temps):
    d = date.fromisoformat(time_str)
    if temp is not None:
        idx[(d.year, d.month, d.day)] = temp

# 3 filtri
exact_vals = [t for (y,m,d), t in idx if (m,d) == target_md]
nearby_vals = [t for (y,m,d), t in idx if nearby_start <= date(2000,m,d) <= nearby_end and (m,d) != target_md]
monthly_vals = [t for (y,m,d), t in idx if m == target_date.month]
```

## Integrazione nel Prompt AI

Il prompt riceve 3 sezioni separate:
```
## Dati climatologici approfonditi
- Media storica (10 anni): 33°C ±2.9°C
- Range: 30-39°C, Record: 29-39°C
- Trend: +3.6°C/decennio

## Statistiche finestra temporale (±5 giorni)
- Media (±5gg, 100 campioni): 33°C ±2.8°C
- Range: 30-36°C

## Analisi clima mensile
- Media mensile (310 campioni): 33°C ±2.9°C
- Record mese: 22°C — 40°C
```

Istruzione finale nel prompt:
> "Usa la finestra ±5gg e l'analisi mensile per **consolidare la percentuale di sicurezza**: più i dati delle 3 scale temporali sono allineati, più alta deve essere la confidenza"

## Pitfall

- **Arrotondamento**: i record del mese (`monthly_record_max_temp_c`, `monthly_record_min_temp_c`) DEVONO essere arrotondati a interi con `round()` prima di passarli a Pydantic, altrimenti il campo `Optional[int]` rifiuta float.
- **Date di confine**: per date come 31 Dicembre o 1 Gennaio, la finestra ±5gg può sconfinare nel mese successivo/precedente. Usa `date(2000, m, d) + timedelta(days=offset)` per i calcoli di prossimità.
- **29 Febbraio**: gestisci con fallback a 28 Febbraio nei `_safe_date()`.
