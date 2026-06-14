# Reconstruction Plan

## First Principles

1. **Information retrieval is solved at the atomic level** — search, extract, synthesize.
2. **User wants a decision-grade cited answer** — not a wall of links.
3. **Pipeline, not architecture** — one script, linear flow.

## Plan

| Step | What | Why |
|------|------|-----|
| 1 | Single `xinxiagent.py` CLI | Musk's razor: no framework, no database |
| 2 | httpx + bs4 for web search/scrape | Atomic tools, zero abstraction |
| 3 | OpenAI SDK for synthesis | LLM turns raw text into cited answer |
| 4 | `requirements.txt` | 3 deps, nothing more |

## Architecture

```
query → DuckDuckGo search → top N pages → extract text → LLM synthesis → cited answer
```

## Constraints

- No RAG, no vector DB, no web framework
- Single script, ~100 lines
- CLI-first: `python xinxiagent.py "your question"`
