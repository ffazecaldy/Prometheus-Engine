# Ollama Integration Patterns

## Response Format — Cloud vs Local Models

Ollama's `/api/generate` endpoint returns different response shapes depending on model type.

### Local models (e.g., `qwen2.5-coder:14b`, `deepseek-r1:14b`)

With `"stream": false, "format": "json"`, the response contains the model's output directly in the `response` field:

```json
{
  "model": "qwen2.5-coder:14b",
  "response": "{\"expected_max_temp_c\": 34.2}",
  "done": true,
  "total_duration": 3200000000,
  "eval_count": 310
}
```

### Cloud models (e.g., `gemma4:31b-cloud`, `glm-5.1:cloud`, `deepseek-v4-flash:cloud`)

Same wrapper format — the actual output is in the `response` field.

## Critical: Extract `response` Field Before JSON Parsing

**Bug pattern:** `response.text` gives the entire Ollama wrapper JSON. If you pass this directly to `json.loads()`, it parses the wrapper into a dict with keys `model`, `response`, `done`, etc. — NOT your expected schema.

**Fix:**

```python
# ❌ WRONG — parses the Ollama wrapper, not the model output
raw = response.text
data = json.loads(raw)  # {model: ..., response: ..., done: ...}

# ✅ RIGHT — extract the model's text output first
payload = response.json()
raw = payload.get("response", response.text)
data = _extract_json(raw)  # {"expected_max_temp_c": ..., ...}
```

## Prompt: Force JSON Output

Use `"format": "json"` in the generate request to constrain output:

```python
client.post(f"{host}/api/generate", json={
    "model": model_name,
    "prompt": prompt,
    "stream": False,
    "format": "json",           # tells Ollama to prefer JSON
})
```

Also add explicit instructions in the prompt:
```
Rispondi SOLO con JSON valido, nessun testo prima o dopo.
```

## JSON Extraction Fallback Strategies

When `format: "json"` is used, most models comply, but some still wrap output in markdown or add commentary. Implement multiple extraction strategies in order:

1. **Direct** — `json.loads(text)` (preferred, works when `format: "json"` works)
2. **Markdown fenced block** — regex ````(?:json)?\s*\n?(.*?)```` to grab code block content
3. **Brace matching** — scan for first top-level `{ ... }` pair for partial/inline JSON

```python
def _extract_json(text: str) -> dict | None:
    # Strategy 1: direct
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strategy 2: markdown code block
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # Strategy 3: brace-match first valid object
    ...
    return None
```

## Subscription / Auth

Cloud models in Ollama (`:cloud` tag) require authentication:

```bash
ollama login          # opens browser for OAuth
ollama login --token TOKEN  # headless auth (token from ollama.com/settings/keys)
```

Some cloud models also require a **paid subscription** — the API returns 403 with message `"this model requires a subscription, upgrade for access: https://ollama.com/upgrade"`.

Check before implementing:

```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"gemma4:31b-cloud","prompt":"test","stream":false}' | jq .error
```

## Timeout Considerations

- Local 14B models on CPU: 3–60+ seconds per inference
- Cloud models: 5–30 seconds (network latency + inference)
- Small local models (7B): 1–5 seconds
- **Set timeout >= 120s** when supporting both local and cloud models
- Increase to 180s for 14B+ local models
- Implement retry with exponential backoff for transient failures

## Available Models Check

```python
async def check_ollama_status() -> OllamaStatus:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.ollama_host}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return OllamaStatus(reachable=True, models=models)
    except Exception as e:
        return OllamaStatus(reachable=False, error=str(e))
```
