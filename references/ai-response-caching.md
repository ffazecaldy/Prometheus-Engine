# AI Response Caching — Pattern SHA256

Cache per risposte di modelli AI (Ollama, OpenAI, Claude) in progetti full-stack.

## Quando serve

- Chiamate AI costose (token, latenza) per input ripetibili
- Utente che ricarica la pagina o ritenta stessa richiesta
- Stessa località+data richiesta da utenti diversi
- Riduzione latency percepita: da 15s a 1s (-92%)

## Pattern base (FastAPI + SQLite)

### Modello (SQLAlchemy)

```python
class OllamaResponseCache(Base):
    __tablename__ = "ollama_response_cache"
    id = Column(Integer, primary_key=True, autoincrement=True)
    luogo = Column(String(255), nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    model_name = Column(String(100), nullable=False, default="")
    expected_max_temp_c = Column(Integer, nullable=False)
    confidence_level = Column(String(10), nullable=False)
    confidence_pct = Column(Integer, default=50)
    confidence_reasoning = Column(String(3000), nullable=True)
    explanation = Column(String(8000), nullable=True)
    probability_distribution = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    hit_count = Column(Integer, default=1)
```

### Cache Key — SHA256

Usa SHA256 per generare chiavi deterministiche:

```python
import hashlib
from datetime import date

def cache_key(luogo: str, target_date: date, model_name: str) -> str:
    raw = f"{luogo.strip().lower()}|{target_date.isoformat()}|{model_name}"
    return hashlib.sha256(raw.encode()).hexdigest()
```

**Vantaggi:** case-insensitive, whitespace-normalized, deterministico, collisioni impossibili.

### TTL

Cache valida per un numero configurabile di ore:

```python
CACHE_TTL_HOURS = 6

async def get_cached(key: str):
    cutoff = datetime.utcnow() - timedelta(hours=CACHE_TTL_HOURS)
    query = select(OllamaResponseCache).where(
        OllamaResponseCache.created_at >= cutoff
    ).order_by(OllamaResponseCache.created_at.desc())
```

### Hit counter

Incrementa `hit_count` a ogni cache hit — utile per vedere se la cache è effettivamente usata.

## Integrazione nel flusso

```
1. Ricevi richiesta con (luogo, data)
2. Calcola cache key
3. Cerca in DB:
   ├─ Hit → salta chiamata AI, restituisci cached
   └─ Miss → chiama AI, salva in cache, restituisci risposta
```

Esempio:

```python
cached = await get_cached_forecast(body.luogo, body.data)
if cached is not None:
    return cached

ai_forecast = await call_ollama(prompt)  # ~15s
await save_ollama_cache(body.luogo, body.data, ai_forecast)
return ai_forecast
```

## Variazioni

- **Redis/Memcached**: per alta concorrenza, sostituisci SQLite con Redis TTL
- **File-based**: JSON su disco per progetti senza DB
- **Content-addressed**: includi hash dei dati sorgente nella chiave per invalidazione fine
