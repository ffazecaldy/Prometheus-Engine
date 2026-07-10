# Ensemble Confidence Scoring — Blended Objective/Subjective

Tecnica per calcolare la confidenza di una previsione AI basandosi su:

- **60% Objective**: accordo tra modelli ensemble + coerenza climatologica
- **40% Subjective**: autovalutazione dell'AI (self-assessment)

## Perché serve

L'autovalutazione dell'AI da sola (confidence_level, confidence_pct) è inaffidabile:
- Modelli diversi danno confidence diverse per lo stesso input
- L'AI può essere sovra-confidente o sotto-confidente
- Non tiene conto del disaccordo tra fonti dati

## Pattern

### 1. Calcola Ensemble Agreement

```python
def ensemble_agreement(sources: list[SourceForecast]) -> float:
    valid = [s.max_temp_c for s in sources if s.max_temp_c is not None]
    if len(valid) < 2:
        return 0.0
    mean = sum(valid) / len(valid)
    deviations = [abs(v - mean) for v in valid]
    avg_dev = sum(deviations) / len(deviations)
    # 0°C deviazione → 100 agreement, 10°C deviazione → 0 agreement
    return max(0, 100 - avg_dev * 10)
```

### 2. Calcola Match Climatologico

```python
if climatology and climatology.mean_max_temp_c is not None and ensemble_mean is not None:
    diff = abs(ensemble_mean - climatology.mean_max_temp_c)
    climatology_match = max(0, 100 - diff * 8)
```

### 3. Blended Score

```python
if climatology_match is not None:
    raw = ensemble_agreement * 0.6 + climatology_match * 0.4
else:
    raw = ensemble_agreement * 0.8

pct = max(10, min(99, round(raw)))

if pct >= 75: level = "alto"
elif pct >= 45: level = "medio"
else: level = "basso"

final_pct = round(objective_pct * 0.6 + ai_self_assessment * 0.4)
```

### 4. Confidence Reasoning

```python
parts = [f"Accordo tra modelli: {agreement}%"]
if climatology_match is not None:
    parts.append(f"Coerenza climatologica: {climatology_match}%")
reasoning = f"Confidenza basata su ensemble: {' + '.join(parts)}. Score: {pct}%."
```

## Caso d'uso reale

```
8 modelli meteo per Milano:
  GFS: 35°C, ICON: 34°C, GEM: 34°C, MF-ARPEGE: 35°C,
  JMA-GSM: 32°C, BOM-Access: N/D, ECMWF: N/D, Meteoblue: 32°C

Ensemble agreement: 88.9%
Climatology match: 68%
Objective score: 88.9*0.6 + 68*0.4 = 81% → "alto"
AI self-assessment: 83%
Final blended: 81*0.6 + 83*0.4 = 82% → "alto"
```
