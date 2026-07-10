---
tags: [prometheus-engine, utente, preferenze, boschi404]
---

# Preferenze Utente — Boschi404

Queste preferenze sono codificate nel loop agentico.

## Regole Fisse (sempre applicate)

- **Lingua**: output SEMPRE in italiano
- **Commit + Push**: dopo ogni modifica, commit granulare + push immediato
- **Test live**: dopo backend change, test con curl/chiamata HTTP reale
- **Temperature 1 decimale**: `round(x, 1)` per betting Polymarket
- **Header UI statico**: non cambia colore con i dati
- **Quick cities → domani**: data preimpostata a oggi+1
- **Storico climatologico**: mediana, percentili, record, trend decennale, anomalia
- **Self-Feedback**: alla fine di ogni task completato, autovalutazione 0-100% su qualità della gestione

## Profilo GitHub
- Username: ffazecaldy
- Repository: PolimarketWeather
- Token GitHub configurato

## Meteoblue
- Chiave API configurata

## Collegamenti
- [[Fase 3 - Streaming Quality Gate]] — Git commit policy
- [[Fase 8 - Final Report]] — Report in italiano
