import os
import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from loader import load_pdf
from chunker import chunk_pages

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index(pdf_file):
    pages = load_pdf(pdf_file)
    chunks = chunk_pages(pages)
    if not chunks:
        raise ValueError("No text found. This PDF may be scanned images.")
    vectors = model.encode([c["text"] for c in chunks])
    vectors = np.array(vectors).astype("float32")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index, chunks


def search(question, index, chunks, top_k=5):
    q_vec = np.array(model.encode([question])).astype("float32")
    faiss.normalize_L2(q_vec)
    scores, ids = index.search(q_vec, top_k)
    return [chunks[i] for i in ids[0] if i != -1]


def answer(question, index, chunks):
    results = search(question, index, chunks)
    context = "\n\n".join(f"[Page {r['page']}]\n{r['text']}" for r in results)

    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I could not find this in the document."
Mention the page number(s) you used.

Context:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content, results