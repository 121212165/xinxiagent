#!/usr/bin/env python3
"""xinxiagent — minimal web information retrieval agent.

Pipeline: query → search → extract → synthesize → cited answer.

Usage:
    python xinxiagent.py "What is Rust's borrow checker?"
    python xinxiagent.py -n 5 "How does CRISPR work?"
"""

import sys
import argparse
import textwrap
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup

DUCKDUCKGO_URL = "https://html.duckduckgo.com/html/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 10


def search(query: str, num_results: int = 5) -> list[dict]:
    """Search DuckDuckGo and return [{title, url, snippet}, ...]."""
    resp = httpx.post(
        DUCKDUCKGO_URL,
        data={"q": query},
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
        follow_redirects=True,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for r in soup.select(".result"):
        link = r.select_one(".result__a")
        snippet = r.select_one(".result__snippet")
        if link and link.get("href"):
            results.append({
                "title": link.get_text(strip=True),
                "url": link["href"],
                "snippet": snippet.get_text(strip=True) if snippet else "",
            })
        if len(results) >= num_results:
            break
    return results


def extract(url: str, max_chars: int = 3000) -> str:
    """Fetch a URL and extract readable text."""
    try:
        resp = httpx.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:max_chars]
    except Exception:
        return ""


def synthesize(query: str, sources: list[dict]) -> str:
    """Use OpenAI to synthesize a cited answer from sources."""
    try:
        from openai import OpenAI
        client = OpenAI()
    except Exception:
        return _fallback_answer(query, sources)

    context_parts = []
    for i, s in enumerate(sources, 1):
        context_parts.append(f"[{i}] {s['title']} — {s['url']}\n{s.get('content', s.get('snippet', ''))}")
    context = "\n\n".join(context_parts)

    prompt = (
        f"Answer the question using ONLY the sources below. "
        f"Cite sources as [1], [2], etc.\n\n"
        f"Question: {query}\n\n"
        f"Sources:\n{context}\n\n"
        f"Answer:"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.2,
    )
    return response.choices[0].message.content


def _fallback_answer(query: str, sources: list[dict]) -> str:
    """Fallback when no LLM is available — return snippets with sources."""
    lines = [f"Query: {query}\n"]
    for i, s in enumerate(sources, 1):
        lines.append(f"[{i}] {s['title']}")
        lines.append(f"    {s['url']}")
        lines.append(f"    {s.get('snippet', '(no snippet)')}\n")
    lines.append("Set OPENAI_API_KEY for synthesized answers.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="xinxiagent — web information retrieval agent")
    parser.add_argument("query", help="Natural language query")
    parser.add_argument("-n", "--num", type=int, default=3, help="Number of results to fetch (default: 3)")
    args = parser.parse_args()

    print(f"Searching: {args.query}")
    results = search(args.query, args.num)
    if not results:
        print("No results found.")
        sys.exit(1)

    print(f"Found {len(results)} results. Extracting content...")
    for r in results:
        r["content"] = extract(r["url"])

    print("Synthesizing answer...\n")
    answer = synthesize(args.query, results)
    print(answer)


if __name__ == "__main__":
    main()
