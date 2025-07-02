from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Stack Overflow RAG Q&A Backend is running (Flask)."})

@app.route("/ask_llm", methods=["POST"])
def ask_llm():
    data = request.get_json()
    question = data.get("question", "")
    # TODO: Generate answer using your LLM
    answer = "This is a sample LLM answer."
    source_url = "https://stackoverflow.com/q/123456"
    response = {"answer": answer, "source_url": source_url}
    return jsonify(response)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    source = data.get("source", "local")
    response = {}

    # DEBUG: Always return a unique answer for testing
    response = {
        "answer": f"DEBUG ANSWER: {question}",
        "sources": [{"question": question, "answer": "DEBUG SOURCE"}],
        "tokens": 2,
        "status": "done"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
