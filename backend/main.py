from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Stack Overflow RAG Q&A Backend is running."}

@app.post("/ask_llm")
async def ask_llm(request: Request):
    data = await request.json()
    question = data.get("question", "")
    # TODO: Generate answer using your LLM
    answer = "This is a sample LLM answer."
    source_url = "https://stackoverflow.com/q/123456"
    return JSONResponse({"answer": answer, "source_url": source_url})

# TODO: Implement /ask endpoint, embedding, retrieval, and Gemini Pro integration
