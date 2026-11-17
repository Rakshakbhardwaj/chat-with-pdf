from loader import load_pdf

def chunk_pages(pages, chunk_size=800, overlap=100):
    chunks = []
    for page_num, text in pages:
        start = 0
        while start < len(text):
            end = start + chunk_size
            piece = text[start:end].strip()
            if piece:
                chunks.append({"page": page_num, "text": piece})
            start = end - overlap
    return chunks

if __name__ == "__main__":
    pages = load_pdf("data/sample.pdf")
    chunks = chunk_pages(pages)
    print("Total chunks:", len(chunks))
    print("--- Chunk 1 ---")
    print(chunks[0])
    print("--- Chunk 2 ---")
    print(chunks[1])