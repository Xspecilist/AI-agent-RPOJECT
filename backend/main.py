# server.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import trafilatura

app = FastAPI()

BRAVE_API_KEY = "BSAYcmGcjd6eznA7um8osQlNpvCfD51"

# CORS setup (allow only your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize summarization pipeline
# Note: loading the model can be slow; prefer to load once at startup as shown here.
summarize_via_hf()

@app.get("/search_summary")
def search_and_summarize(
    q: str = Query(..., description="Search query"),
    country: str = Query("US", description="Country code (e.g., US, BE, IN)"),
    ui_lang: str = Query("en-US", description="UI language (e.g., en-US, fr-FR, hi-IN)"),
):
    """
    Search Brave Web API with optional country and ui_lang, fetch pages,
    extract text, and summarize each page using the HF summarization pipeline.
    Returns results list and a combined_summary.
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    # pass query, country and ui_lang to Brave API
    params = {"q": q, "count": 7, "country": country, "ui_lang": ui_lang}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}

    data = response.json()
    results = []
    url_summaries = []

    for item in data.get("web", {}).get("results", [])[:7]:
        url_item = item.get("url")
        content_preview = None
        summary = None

        try:
            # fetch and extract
            downloaded = trafilatura.fetch_url(url_item)
            if downloaded:
                extracted = trafilatura.extract(downloaded)
                if extracted:
                    # Truncate to 900 characters for faster summarization
                    content_preview = extracted[:900]
                    # Generate summary (no explicit min/max length, model default)
                    try:
                        out = summarizer(content_preview, do_sample=False)
                        # pipeline returns list of dicts with 'summary_text'
                        if out and isinstance(out, list):
                            summary = out[0].get("summary_text")
                    except Exception as s_err:
                        summary = f"Summarization error: {s_err}"
                    if summary:
                        url_summaries.append(summary)
        except Exception as e:
            content_preview = f"Error extracting: {str(e)}"

        results.append(
            {
                "title": item.get("title"),
                "url": url_item,
                "description": item.get("description"),
                "content_preview": content_preview,
                "summary": summary,
            }
        )

    # Combine all URL summaries into a single text
    combined_summary = " ".join(url_summaries) if url_summaries else None

    return {"query": q, "country": country, "ui_lang": ui_lang, "results": results, "combined_summary": combined_summary}
