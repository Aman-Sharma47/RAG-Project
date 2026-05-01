import hashlib
import os

from src.data_loader import list_supported_files, load_documents_from_files
from src.search import RAGSearch
from src.vectorstore import FaissVectorStore


def build_persist_dir(selected_files):
    digest_input = "|".join(str(path) for path in selected_files)
    digest = hashlib.md5(digest_input.encode("utf-8")).hexdigest()[:12]
    return os.path.join("faiss_store", digest)


def choose_files(data_dir: str):
    files = list_supported_files(data_dir)
    if not files:
        raise ValueError("No supported documents found in the 'data' folder.")

    print("Available files:")
    for index, file_path in enumerate(files, start=1):
        print(f"{index}. {file_path.name}")

    selection = input("Select file numbers separated by commas, or type 'all': ").strip().lower()
    if selection == "all":
        return files

    selected_indexes = []
    for part in selection.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            raise ValueError("Invalid selection. Use numbers like 1,2 or type 'all'.")
        selected_indexes.append(int(part))

    selected_files = []
    for idx in selected_indexes:
        if idx < 1 or idx > len(files):
            raise ValueError("Selected file number is out of range.")
        selected_files.append(files[idx - 1])

    if not selected_files:
        raise ValueError("No files selected.")
    return selected_files


def ensure_vectorstore(persist_dir: str, selected_files):
    store = FaissVectorStore(persist_dir)
    faiss_path = os.path.join(persist_dir, "faiss.index")
    meta_path = os.path.join(persist_dir, "metadata.pkl")

    if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
        docs = load_documents_from_files(selected_files)
        if not docs:
            raise ValueError("No readable content found in the selected files.")
        store.build_from_documents(docs)
    else:
        store.load()

    return store


if __name__ == "__main__":
    selected_files = choose_files("data")
    print("Selected files:")
    for file_path in selected_files:
        print(f"- {file_path.name}")

    persist_dir = build_persist_dir(selected_files)
    ensure_vectorstore(persist_dir, selected_files)

    rag_search = RAGSearch(persist_dir=persist_dir)
    while True:
        query = input("Enter your question (or type 'exit' to quit): ").strip()
        if not query:
            print("Please enter a question.")
            continue
        if query.lower() in {"exit", "quit"}:
            break

        result = rag_search.answer_question(query, top_k=3)
        print("\nAnswer:", result["answer"])
        if result["sources"]:
            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source['label']}")
        print()
