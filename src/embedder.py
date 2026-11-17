from sentence_transformers import SentenceTransformer
from chunker import chunk_pages
from loader import load_pdf

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    return model.encode(texts)

if __name__ == "__main__":
    pages = load_pdf("data/sample.pdf")
    chunks = chunk_pages(pages)
    texts = [c["text"] for c in chunks]

    vectors = embed_texts(texts)
    print("Number of vectors:", len(vectors))
    print("Size of each vector:", len(vectors[0]))
    print("First 5 numbers of vector 1:", vectors[0][:5])