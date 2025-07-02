from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_qa_collection
from app.gemini import generate_gemini_answer
from chromadb import Client

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: list
    tokens: int

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    # 1. Embed the question (placeholder)
    # 2. Retrieve top 3 similar Q&A pairs from ChromaDB
    collection = get_qa_collection()
    # Placeholder: just return empty sources
    sources = []
    # 3. Compose prompt for Gemini Pro
    prompt = f"Question: {request.question}\n\nSources: {sources}"
    # 4. Generate answer
    try:
        answer = await generate_gemini_answer(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # 5. Return response
    return AskResponse(answer=answer, sources=sources, tokens=len(answer.split()))
