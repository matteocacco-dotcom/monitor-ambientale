import os
import json
from datetime import datetime, timezone
from tavily import TavilyClient
from groq import Groq

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Modifica/aggiungi query a piacere
QUERIES = [
    "nuovi progetti ambientali innovativi",
    "progetti riforestazione e tutela ambientale recenti",
    "iniziative energia rinnovabile comunità locali",
]

MAX_PROJECTS = 12

tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)


def search_projects():
    results = []
    for q in QUERIES:
        res = tavily.search(
            query=q,
            search_depth="basic",
            max_results=5,
            days=14,  # solo notizie recenti
        )
        results.extend(res.get("results", []))
    return results


def summarize(item):
    prompt = (
        "Riassumi in italiano, in massimo 3 frasi, il seguente articolo "
        "su un progetto ambientale. Rispondi solo con il riassunto, "
        "senza introduzioni o premesse.\n\n"
        f"Titolo: {item.get('title')}\n"
        f"Contenuto: {item.get('content', '')[:2000]}"
    )
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=200,
    )
    return completion.choices[0].message.content.strip()


def main():
    raw_results = search_projects()

    seen_urls = set()
    projects = []

    for item in raw_results:
        url = item.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        try:
            summary = summarize(item)
        except Exception as e:
            print(f"Errore riassunto per {url}: {e}")
            summary = (item.get("content", "") or "")[:300]

        projects.append({
            "title": item.get("title", "Senza titolo"),
            "url": url,
            "summary": summary,
        })

        if len(projects) >= MAX_PROJECTS:
            break

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "projects": projects,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Salvati {len(projects)} progetti.")


if __name__ == "__main__":
    main()