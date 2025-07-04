from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import arxiv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/papers/")
def get_papers(query: str):
    search = arxiv.Search(query=query, max_results=5)
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id
        })
    return results
