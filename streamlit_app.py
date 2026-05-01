import streamlit as st

from app import build_persist_dir, ensure_vectorstore
from src.data_loader import list_supported_files
from src.search import RAGSearch


st.set_page_config(page_title="RAG Chat", layout="wide")
st.title("RAG Chat Over Your Documents")

files = list_supported_files("data")
file_names = [file_path.name for file_path in files]

if not files:
    st.error("No supported files found in the data folder.")
    st.stop()

selected_names = st.multiselect("Select files to query", file_names, default=file_names[:1])
top_k = st.slider("Top chunks to retrieve", min_value=1, max_value=5, value=3)

if not selected_names:
    st.info("Select at least one file to continue.")
    st.stop()

selected_files = [file_path for file_path in files if file_path.name in selected_names]
persist_dir = build_persist_dir(selected_files)

with st.spinner("Preparing vector store..."):
    ensure_vectorstore(persist_dir, selected_files)
    rag_search = RAGSearch(persist_dir=persist_dir)

query = st.text_input("Ask a question about the selected files")

if query:
    with st.spinner("Searching and generating answer..."):
        result = rag_search.answer_question(query, top_k=top_k)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    if result["sources"]:
        for source in result["sources"]:
            with st.expander(source["label"]):
                st.write(source["text"])
    else:
        st.write("No relevant sources found.")
