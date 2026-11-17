import faiss
import numpy as np
from loader import load_pdf
from chunker import chunk_pages
from embedder import embed_texts

# Build the index once
pages = load_pdf("data/sample.pdf")
chunks = chunk_pages(pages)
texts = [c["text"] for c in chunks]

vectors = embed_texts(texts)
vectors = np.array(vectors).astype("float32")

faiss.normalize_L2(vectors)
index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)

def search(question, top_k=5):
    q_vec = np.array(embed_texts([question])).astype("float32")
    faiss.normalize_L2(q_vec)
    scores, ids = index.search(q_vec, top_k)
    return [chunks[i] for i in ids[0]]

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'quit'): ")
        if q.lower() == "quit":
            break
        for r in search(q):
            print(f"\n[Page {r['page']}]")
            print(r["text"][:300])