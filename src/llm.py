import os
from dotenv import load_dotenv
from groq import Groq
from search import search

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer(question):
    results = search(question, top_k=5)
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
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        print("\n" + answer(q))