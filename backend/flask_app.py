from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    return jsonify({"answer": answer, "source_url": source_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
