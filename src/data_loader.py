from pathlib import Path
from typing import List, Any, Iterable
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader


SUPPORTED_PATTERNS = ["*.pdf", "*.txt", "*.csv", "*.xlsx", "*.docx", "*.json"]


def list_supported_files(data_dir: str) -> List[Path]:
    data_path = Path(data_dir).resolve()
    files = []
    for pattern in SUPPORTED_PATTERNS:
        files.extend(data_path.glob(f"**/{pattern}"))
    return sorted({file.resolve() for file in files})


def _load_file(file_path: Path) -> List[Any]:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif suffix == ".txt":
        loader = TextLoader(str(file_path))
    elif suffix == ".csv":
        loader = CSVLoader(str(file_path))
    elif suffix == ".xlsx":
        loader = UnstructuredExcelLoader(str(file_path))
    elif suffix == ".docx":
        loader = Docx2txtLoader(str(file_path))
    elif suffix == ".json":
        loader = JSONLoader(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    loaded = loader.load()
    for doc in loaded:
        doc.metadata.setdefault("source", str(file_path))
    return loaded


def load_documents_from_files(file_paths: Iterable[Path]) -> List[Any]:
    documents = []
    for file_path in file_paths:
        print(f"[DEBUG] Loading file: {file_path}")
        try:
            loaded = _load_file(Path(file_path).resolve())
            print(f"[DEBUG] Loaded {len(loaded)} docs from {file_path}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load {file_path}: {e}")
    print(f"[DEBUG] Total loaded documents: {len(documents)}")
    return documents

def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load all supported files from the data directory and convert to LangChain document structure.
    Supported: PDF, TXT, CSV, Excel, Word, JSON
    """
    data_path = Path(data_dir).resolve()
    print(f"[DEBUG] Data path: {data_path}")
    files = list_supported_files(data_dir)
    print(f"[DEBUG] Found {len(files)} supported files: {[str(f) for f in files]}")
    return load_documents_from_files(files)

# Example usage
if __name__ == "__main__":
    docs = load_all_documents("data")
    print(f"Loaded {len(docs)} documents.")
    print("Example document:", docs[0] if docs else None)
