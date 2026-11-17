import streamlit as st
from rag import build_index, answer

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")
st.title("📄 Chat with your PDF")

uploaded = st.file_uploader("Upload a PDF", type="pdf")

if uploaded:
    if st.session_state.get("file_name") != uploaded.name:
        with st.spinner("Reading your PDF..."):
            try:
                index, chunks = build_index(uploaded)
            except ValueError as e:
                st.error(str(e))
                st.stop()
        st.session_state.file_name = uploaded.name
        st.session_state.index = index
        st.session_state.chunks = chunks
        st.success(f"Ready! Split into {len(chunks)} chunks.")

    question = st.text_input("Ask a question about your PDF")

    if question:
        with st.spinner("Thinking..."):
            reply, sources = answer(
                question, st.session_state.index, st.session_state.chunks
            )
        st.markdown(reply)
        with st.expander("Show sources"):
            for s in sources:
                st.markdown(f"**Page {s['page']}**")
                st.write(s["text"])