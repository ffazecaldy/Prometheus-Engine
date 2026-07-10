---
tags: [prometheus-engine, pattern, ollama, AI]
---

# Ollama Integration

Pattern per chiamare Ollama con parsing JSON robusto.

## Extraction JSON (3 strategie)
1. `json.loads()` diretto
2. Regex ` ```json ... ``` `
3. Brace-matching: primo `{...}` top-level

## Retry con Feedback
Se JSON non valido → riprova con hint "Rispondi SOLO con JSON valido"
Max 3 tentativi, timeout configurabile (default 180s)

## Response Wrapper
La risposta HTTP Ollama è `{"model":"...", "response":"...", "done":true}`.
Estrarre SEMPRE `payload.get("response")` prima del parsing.

## Cloud Models
I modelli `:cloud` richiedono `ollama login` e abbonamento. Verifica con curl prima.

## Collegamenti
- [[AI Response Caching]] — Cache per evitare chiamate ripetute
- [[Ensemble Confidence Scoring]] — AI self-assessment
- [[External API Integration]] — Pattern generale per API
