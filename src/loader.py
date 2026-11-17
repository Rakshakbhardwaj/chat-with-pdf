from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text.strip():
            pages.append((i, text))
    return pages

if __name__ == "__main__":
    pages = load_pdf("data/sample.pdf")
    print("Total pages with text:", len(pages))
    print("--- Page 1 preview ---")
    print(pages[0][1][:500])