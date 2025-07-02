from flask import Flask, request, jsonify
from flask_cors import CORS
from datasets import load_dataset
from functools import lru_cache
import logging
import json
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Stack Overflow RAG Q&A Backend is running (Flask)."})

@app.route("/ask_llm", methods=["POST"])
def ask_llm():
    data = request.get_json()
    logging.info(f"/ask_llm request: {data}")
    question = data.get("question", "")
    # TODO: Generate answer using your LLM
    answer = "This is a sample LLM answer."
    source_url = "https://stackoverflow.com/q/123456"
    response = {"answer": answer, "source_url": source_url}
    logging.info(f"/ask_llm response: {response}")
    return jsonify(response)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    logging.info(f"/ask request: {data}")
    question = data.get("question", "")
    source = data.get("source", "hf")
    tags = data.get("tags")  # Optional: list of tags to filter by
    min_score = data.get("min_score", 0)  # Optional: minimum score
    response = {}

    @lru_cache(maxsize=128)
    def cached_hf_results(question, tags_str, min_score):
        logging.info("[HF] Starting Hugging Face streaming QA...")
        try:
            ds = load_dataset("mikex86/stackoverflow-posts", split="train", streaming=True)
            results = []
            question_lc = question.lower()
            tags_set = set([t.strip().lower() for t in tags_str.split(",") if t.strip()]) if tags_str else set()
            max_items = 2000
            for i, item in enumerate(ds):
                if i >= max_items:
                    break
                # Use lowercase field names for HF dataset
                title = item.get("question", "")
                body = item.get("answer", "")
                tags = item.get("tags", [])
                score = item.get("score", 0)
                title_lc = title.lower() if isinstance(title, str) else ""
                body_lc = body.lower() if isinstance(body, str) else ""
                tags_lc = [t.lower() for t in tags] if isinstance(tags, list) else []
                # Match if question in title, body, or tags
                tag_match = any(question_lc in t for t in tags_lc)
                text_match = (question_lc in title_lc and title_lc) or (question_lc in body_lc and body_lc)
                if (text_match or tag_match) and (title_lc or body_lc):
                    # Tag filter
                    if tags_set and not tags_set.intersection(set(tags_lc)):
                        continue
                    # Score filter
                    if score < min_score:
                        continue
                    results.append({
                        "question": title,
                        "answer": body,
                        "tags": tags,
                        "score": score
                    })
                if i % 100 == 0:
                    logging.info(f"[HF] Processed {i} items, found {len(results)} matches so far.")
            # Sort by score descending
            results.sort(key=lambda x: x["score"] if x.get("score") is not None else 0, reverse=True)
            logging.info(f"[HF] Done. Found {len(results)} results.")
            return results[:3]
        except Exception as e:
            logging.error(f"[HF] Error: {str(e)}")
            return []

    if source == "local":
        # Load from local JSON file (e.g., backend/data/localdata.json)
        try:
            with open(os.path.join(os.path.dirname(__file__), "../data/localdata.json"), "r") as f:
                local_data = json.load(f)
            # For demo, just return the first item that matches the question substring
            matches = [item for item in local_data if question.lower() in item.get("question", "").lower()]
            sources = matches[:3] if matches else local_data[:3]
            answer = sources[0]["answer"] if sources else "No local answer found."
            response = {
                "answer": answer,
                "sources": sources,
                "tokens": len(answer.split()),
                "status": "done"
            }
        except Exception as e:
            logging.error(f"Local source error: {e}")
            response = {"answer": "Local data error.", "sources": [], "tokens": 0, "status": "error"}
    elif source == "hf":
        try:
            tags_str = ",".join(tags) if tags else ""
            logging.info(f"HF streaming: question='{question}', tags={tags}, min_score={min_score}")
            results = cached_hf_results(question, tags_str, min_score)
            logging.info(f"HF streaming: got {len(results)} results")
            sources = results if results else []
            answer = sources[0]["answer"] if sources else "No HF answer found."
            response = {
                "answer": answer,
                "sources": sources,
                "tokens": len(answer.split()),
                "status": "done"
            }
            logging.info(f"HF response: {response}")
        except Exception as e:
            logging.error(f"HF source error: {e}")
            response = {"answer": "HF data error.", "sources": [], "tokens": 0, "status": "error"}
    else:
        response = {"answer": "Unknown source.", "sources": [], "tokens": 0, "status": "error"}
    logging.info(f"/ask response: {response}")
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
