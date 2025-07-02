from datasets import load_dataset
import json

def fetch_hf_stackoverflow(topic_keywords, max_pairs=150, out_path=None):
    """
    Download and filter Stack Overflow Q&A pairs from Hugging Face by keywords.
    Args:
        topic_keywords: list of keywords to filter questions (e.g. ["python", "kubernetes", "terraform"])
        max_pairs: max number of Q&A pairs to save
        out_path: where to save the filtered data (json)
    """
    ds = load_dataset("mikex86/stackoverflow-posts", split="train")
    filtered = []
    for item in ds:
        q = item.get("question", "").lower()
        if any(kw in q for kw in topic_keywords):
            filtered.append({"question": item["question"], "answer": item["answer"]})
        if len(filtered) >= max_pairs:
            break
    if out_path:
        with open(out_path, "w") as f:
            json.dump(filtered, f, indent=2)
    return filtered

if __name__ == "__main__":
    # Example usage
    fetch_hf_stackoverflow(
        ["python", "kubernetes", "terraform"],
        max_pairs=150,
        out_path="../data/stackoverflow_hf.json"
    )
