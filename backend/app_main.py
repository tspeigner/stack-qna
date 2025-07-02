from flask import Flask, request, jsonify
from app.gemini import generate_gemini_answer
from dotenv import load_dotenv
import os
import asyncio
import json
from datasets import load_dataset

load_dotenv()

# Load local data if available
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'localdata.json')
qa_data = None
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, 'r') as f:
        qa_data = json.load(f)

def stream_hf_qa(question, keywords=None, max_results=3, max_items=2000):
    print("[HF] Starting Hugging Face streaming QA...")
    status = "starting"
    try:
        status = "downloading dataset info"
        print("[HF] Downloading dataset info from Hugging Face...")
        ds = load_dataset("mikex86/stackoverflow-posts", split="train", streaming=True)
        status = "searching"
        print(f"[HF] Searching for matches for question: '{question}' (max_items={max_items})")
        results = []
        question_lc = question.lower()
        count = 0
        for item in ds:
            count += 1
            if count <= 5:
                print(f"[HF] Example {count}: Title={str(item.get('Title', ''))[:80]} | Body={str(item.get('Body', ''))[:60]}")
            if count % 10 == 0:
                print(f"[HF] Processed {count} items...")
            title = item.get("Title") or ""
            body = item.get("Body") or ""
            tags = item.get("Tags") or []
            score = item.get("Score", 0)
            favs = item.get("FavoriteCount", 0)
            accepted = item.get("AcceptedAnswerId")
            title_lc = title.lower() if isinstance(title, str) else ""
            body_lc = body.lower() if isinstance(body, str) else ""
            tags_lc = [t.lower() for t in tags] if isinstance(tags, list) else []
            # Match if question in title, body, or tags
            tag_match = any(question_lc in t for t in tags_lc)
            text_match = (question_lc in title_lc and title_lc) or (question_lc in body_lc and body_lc)
            if (text_match or tag_match) and (title_lc or body_lc):
                print(f"[HF] Match found: {title_lc[:60]} | {body_lc[:60]} | tags={tags_lc}")
                results.append({
                    "question": title or body,
                    "answer": body,
                    "tags": tags,
                    "score": score,
                    "favorite_count": favs,
                    "accepted_answer_id": accepted
                })
            if count >= max_items:
                print(f"[HF] Reached max_items ({max_items}), stopping search.")
                break
        # Sort: accepted answer first, then score, then favorites
        results.sort(key=lambda x: (
            x["accepted_answer_id"] is not None,
            x["score"] if x["score"] is not None else 0,
            x["favorite_count"] if x["favorite_count"] is not None else 0
        ), reverse=True)
        status = "done"
        print(f"[HF] Done. Found {len(results)} results.")
        return {"results": results[:max_results], "status": status}
    except Exception as e:
        status = f"error: {str(e)}"
        print(f"[HF] Error: {str(e)}")
        return {"results": [], "status": status}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Stack Overflow RAG Q&A Backend is running."})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    source = data.get("source", "hf")  # 'hf', 'local', or 'llm'
    if not question:
        return jsonify({"error": "Missing question"}), 400
    status = "processing"
    sources = []
    if source == "local":
        if qa_data is None:
            return jsonify({"error": "Local data file not found. Please generate it first."}), 500
        sources = [item for item in qa_data if question.lower() in item["question"].lower()]
        if not sources:
            sources = qa_data[:3]
        status = "done"
    elif source == "hf":
        hf_result = stream_hf_qa(question)
        if not hf_result or not isinstance(hf_result, dict):
            return jsonify({"error": "HF streaming failed", "status": "error"}), 500
        sources = hf_result.get("results", [])
        status = hf_result.get("status", "error")
    elif source == "llm":
        sources = []  # Placeholder for future Gemini/OpenAI direct LLM integration
        status = "llm placeholder"
    else:
        return jsonify({"error": "Invalid source option"}), 400
    prompt = f"Question: {question}\n\nSources: {sources}"
    try:
        answer = asyncio.run(generate_gemini_answer(prompt))
    except Exception as e:
        if sources:
            answer = sources[0]["answer"]
        else:
            answer = "Sorry, I couldn't find an answer."
    return jsonify({
        "answer": answer,
        "sources": sources,
        "tokens": len(answer.split()),
        "status": status
    })

@app.route("/hf_health", methods=["GET"])
def hf_health():
    try:
        ds = load_dataset("mikex86/stackoverflow-posts", split="train", streaming=True)
        first_item = next(iter(ds))
        return jsonify({
            "status": "ok",
            "sample_title": first_item.get("Title", ""),
            "sample_body": first_item.get("Body", "")
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
