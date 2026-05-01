# Beginner Guide to This RAG Project

## What This File Is For

This file is written in very simple language so you can understand the project before your evaluation. Read this file once or twice and you will be able to explain the project confidently even if you are new to RAG.

---

## 1. What is RAG?

RAG means **Retrieval-Augmented Generation**.

Break the name into 2 parts:

1. **Retrieval** = first find relevant information from documents
2. **Generation** = then use an LLM to generate the final answer

Simple meaning:

If I ask a question, the system should not answer only from memory. It should first search my uploaded files, find the useful text, and then answer from that text.

That is RAG.

---

## 2. Why RAG is Needed

Normal LLM problem:

- it may not know my PDF
- it may guess
- it may give general answers
- it may hallucinate

RAG solves this by doing:

- read my files
- store their meaning
- search relevant parts
- give those parts to the LLM
- LLM answers using that context

So if your teacher asks:

**Why did you use RAG?**

Say:

> I used RAG because a normal LLM does not know my custom documents. RAG first retrieves relevant content from my files and then uses that content to generate a better answer.

---

## 3. Very Simple Real-Life Example

Suppose in a startup company there are three documents:

- HR policy
- leave policy
- finance rules

Now an employee asks:

**What is the leave policy?**

If you directly ask an LLM, it may give a general leave policy.

But with RAG:

1. system searches uploaded documents
2. finds the leave policy text
3. sends that text to the LLM
4. LLM gives answer from the actual company document

That is the exact idea shown in your screenshot.

---

## 4. Difference Between Fine-Tuning and RAG

Your teacher may ask this.

### Fine-Tuning

- changes the model itself
- expensive
- needs training data
- slower to update

### RAG

- does not retrain the model
- only adds external knowledge
- cheaper
- easier to update
- good for document question answering

Short answer for viva:

> Fine-tuning changes model behavior by training it again, while RAG keeps the model same and only gives relevant external context before generating the answer.

---

## 5. Full Project Flow in One Look

This is your project flow:

1. files go inside `data` folder
2. project reads those files
3. text is split into chunks
4. each chunk is converted into embedding vectors
5. vectors are stored in FAISS
6. user asks question
7. question is also converted into vector
8. similar chunks are retrieved
9. retrieved context is sent to Groq LLM
10. LLM writes final answer

This one flow is the heart of your whole project.

---

## 6. What is Data Ingestion?

Data ingestion means:

**bringing data into the system**

In your project, data ingestion is:

- reading PDF
- reading TXT
- reading CSV
- reading XLSX
- reading DOCX
- reading JSON

In simple words:

> Data ingestion is the process of collecting and loading documents into the RAG pipeline.

---

## 7. What is Parsing?

Parsing means extracting useful readable content from a file.

Example:

- a PDF file is not directly plain text
- first we extract the text from the PDF
- then we process that text

So parsing is basically converting raw file content into usable text.

---

## 8. What is Chunking?

Chunking means breaking a large document into smaller pieces.

Why needed?

- one full PDF may be too long
- searching whole PDF as one block is not effective
- smaller pieces are better for retrieval

Your project uses:

- chunk size = 1000
- chunk overlap = 200

Meaning:

- each text piece is around 1000 characters
- next piece repeats 200 characters from previous one

Why overlap?

Because if one important sentence is between two chunks, overlap helps not lose meaning.

---

## 9. What is an Embedding?

This is one of the most important viva topics.

Embedding means:

**converting text into numbers so a machine can understand meaning**

Suppose these 2 sentences are similar:

- "What model is used in this project?"
- "Which model has been selected?"

They use different words but have similar meaning.

Embeddings help the computer understand this similarity.

In your project:

- chunk text -> vector
- question text -> vector
- then vectors are compared

Short viva answer:

> An embedding is a dense vector representation of text that captures semantic meaning, so similar text gets similar vector values.

---

## 10. What is FAISS?

FAISS is the vector store used in your project.

Full form:

**Facebook AI Similarity Search**

What FAISS does:

- stores vectors
- searches similar vectors quickly
- helps retrieve relevant chunks

Simple explanation:

> FAISS is used to store document embeddings and perform similarity search between the user query and document chunks.

---

## 11. What is Similarity Search?

When the user asks a question, the system does not search only by exact words.

Instead:

- it converts the question into a vector
- compares it with stored document vectors
- finds the nearest vectors

Nearest means most semantically similar.

This is called similarity search.

---

## 12. What is Context in RAG?

Context means the retrieved text that is given to the LLM before it answers.

In your project:

- top chunks are retrieved
- those chunks are joined together
- joined text becomes context

Then the LLM sees:

- user question
- retrieved context

and gives the answer.

Without context, it may guess.
With context, it becomes more accurate.

---

## 13. What is Groq Doing Here?

Groq is the platform used to run the language model fast through API.

In your project:

- Groq hosts the LLM
- your code sends question + context to Groq
- Groq returns the answer

Current model used:

- `llama-3.1-8b-instant`

---

## 14. Traditional RAG vs Your Project

Your project is a **traditional RAG pipeline**.

Traditional RAG means:

- retrieve relevant chunks first
- send them to LLM
- LLM generates final answer

This is exactly what your project does.

---

## 15. What Happens When You Run the Project

When you run:

```powershell
.\.venv\Scripts\python app.py
```

This happens step by step:

1. `app.py` starts
2. it checks whether `faiss_store` already exists
3. if vector store is missing, it loads files from `data`
4. document chunks are created
5. embeddings are generated
6. FAISS index is built and saved
7. `RAGSearch()` object is created
8. terminal asks you for a question
9. your question is converted to vector
10. top similar chunks are retrieved
11. Groq LLM receives context + question
12. final answer is printed

---

## 16. File-by-File Code Explanation

Now the most important part for understanding the code.

### `app.py`

This is the main file.

What it does:

- imports document loader, vector store, and RAG search class
- checks if FAISS index exists
- if not, it builds the index from documents
- then starts an input loop for user questions
- prints answers

Simple meaning:

> `app.py` controls the complete project and acts like the entry point.

### `src/data_loader.py`

This file reads files from the `data` folder.

It supports:

- PDF
- TXT
- CSV
- XLSX
- DOCX
- JSON

It uses LangChain loaders to convert all these file types into document objects.

Simple meaning:

> `data_loader.py` is responsible for reading user files and preparing them for the RAG pipeline.

### `src/embedding.py`

This file does two main things:

1. chunk the documents
2. generate embeddings

It uses:

- `RecursiveCharacterTextSplitter`
- `SentenceTransformer`

Simple meaning:

> `embedding.py` converts raw document text into searchable vector form.

### `src/vectorstore.py`

This file builds the FAISS vector store.

Main work:

- create FAISS index
- add embedding vectors
- save index to disk
- load index from disk
- search similar vectors

Simple meaning:

> `vectorstore.py` stores document knowledge in vector form and makes retrieval possible.

### `src/search.py`

This file is where actual RAG happens.

Main work:

- load FAISS store
- load Groq LLM
- retrieve top chunks for query
- build prompt with context
- ask LLM
- return final answer

Simple meaning:

> `search.py` connects retrieval and generation.

---

## 17. Code Logic in Very Simple Language

Think of your project like this:

### Stage 1: Build Knowledge Base

- take files
- read text
- cut into pieces
- convert into vectors
- save inside FAISS

### Stage 2: Answer Questions

- take user question
- convert to vector
- search similar text pieces
- give them to LLM
- get final answer

That is your entire project in the easiest possible way.

---

## 18. Why We Delete `faiss_store`

This is important.

When you change files in `data`, the old vector index is still saved.

So if you add a new PDF or remove a file, the FAISS index may still contain old data.

That is why before rebuilding, we run:

```powershell
Remove-Item -Recurse -Force .\faiss_store
```

This forces the project to build a fresh vector database from the current files.

---

## 19. Exact Commands You Should Know

### Go to project folder

```powershell
cd "C:\Users\Aman Sharma\Downloads\RAG_Development"
```

### Delete old index if files changed

```powershell
Remove-Item -Recurse -Force .\faiss_store
```

### Run project

```powershell
.\.venv\Scripts\python app.py
```

### Ask question in terminal

Example:

```text
What is the objective of this project?
```

### Exit

```text
exit
```

---

## 20. Questions You Can Ask From Your PDF

Since your current PDF is about retail analytics and computer vision, you can ask:

- What is the objective of the project?
- Which model is used in the report?
- What are the selected object categories?
- What are the limitations of the model?
- What is the future scope?
- What is the application domain?
- What is the dataset source?

If your question matches the uploaded document, the answer will be better.

---

## 21. What to Say During Evaluation

If teacher asks **Explain your project in simple words**, say:

> My project is a document-based RAG system. I upload files like PDF or text into a local folder. The system reads the files, breaks the content into chunks, converts them into embeddings, and stores them in a FAISS vector store. When I ask a question, the system retrieves the most relevant chunks and sends them as context to a large language model through Groq. The model then generates an answer from my uploaded documents.

If teacher asks **What is the innovation here?**, say:

> The innovation is that instead of asking a general chatbot, I built a custom question answering pipeline over local documents using retrieval, embeddings, vector search, and LLM-based generation.

If teacher asks **Why is this better than direct prompting?**, say:

> It is better because direct prompting may produce generic or hallucinated answers, while RAG first retrieves relevant data from the uploaded documents and then answers using that context.

---

## 22. Important Technical Terms You Must Remember

Memorize these short meanings.

- **RAG**: Retrieval-Augmented Generation
- **Chunking**: splitting long text into smaller parts
- **Embedding**: vector representation of text meaning
- **Vector Store**: storage for embeddings
- **FAISS**: library used for vector similarity search
- **Retrieval**: fetching relevant text chunks
- **Context**: retrieved chunks sent to LLM
- **LLM**: large language model
- **Groq**: platform used to run the LLM
- **Semantic Search**: search by meaning, not only exact keywords

---

## 23. Code Explanation for Viva in Short

If the examiner asks for code explanation, say this:

> The project is divided into modular files. `data_loader.py` loads documents from the data folder and supports selected-file loading. `embedding.py` splits documents into chunks and converts them into embeddings using `all-MiniLM-L6-v2`. `vectorstore.py` stores those embeddings in FAISS and preserves source metadata. `search.py` combines retrieval with Groq LLM generation and returns answers with citations. `app.py` is the main terminal file with file selection support, and `streamlit_app.py` gives a browser-based UI.

---

## 24. Common Mistakes to Avoid in Demo

1. Do not ask unrelated questions if the PDF does not contain that answer.
2. If you add new files, delete `faiss_store` before rerunning.
3. Keep internet on because Groq API needs network.
4. Do not remove `.env` because it contains your API key.
5. If answer seems weird, ask a more document-specific question.

---

## 25. Limitations You Should Honestly Mention

It is good to mention limitations in evaluation.

Say:

> This is a local traditional RAG system with a basic Streamlit UI and basic source citation support. However, it still does not include advanced reranking, OCR, enterprise security, or production deployment features.

This makes your explanation mature and honest.

---

## 26. Future Improvements You Can Mention

If teacher asks what next, say:

1. improve the current Streamlit UI
2. improve the current source citation system
3. support multiple users
4. use hybrid retrieval
5. use better reranking
6. deploy as a campus study assistant

---

## 27. 2-Minute Viva Summary

Memorize this almost exactly:

> My mini project is a Retrieval-Augmented Generation system for answering questions from custom documents. I used Python, LangChain document loaders, Sentence Transformers for embeddings, FAISS for vector similarity search, Groq for final LLM response generation, and Streamlit for a user interface. The workflow is: load documents, split them into chunks, convert chunks into embeddings, store them in FAISS, retrieve top relevant chunks for a user query, and send those chunks as context to the LLM. The final version also supports file selection and source citations with page numbers where available. This makes the answer more grounded in the uploaded files and reduces generic responses.

---

## 28. Last-Minute Rapid Revision Points

- RAG = retrieval + generation
- retrieval first, answer later
- embeddings = text to vectors
- FAISS = vector search engine
- Groq = LLM provider
- chunking improves retrieval
- delete `faiss_store` when data changes
- ask questions related to uploaded file
- use file selection when multiple files exist
- show citations to prove grounding

---

## 29. Final Confidence Note

You do not need to act like an expert in deep AI mathematics. For evaluation, if you clearly explain:

- what problem you solved
- how files are processed
- why embeddings are used
- why FAISS is used
- how retrieval works
- how Groq generates answer

then you will already sound confident and prepared.

Read this file once before sleeping and once before evaluation.

---

## 30. What Exactly Changed In The Final Version

At first, the project was only a simple terminal RAG app. After improvement, it now has:

1. file-by-file selection
2. source citations with page numbers where possible
3. a Streamlit chat UI
4. cleaner answer generation from selected files only

So if someone asks whether this is just a raw demo, say:

> No, the final version includes document selection, source-aware answering, and both terminal and Streamlit interfaces.

---

## 31. Full End-to-End Working of the Project

This section explains everything in order.

### Step 1: You put files inside `data`

Example:

- `report.pdf`
- `notes.txt`
- `summary.docx`

These are the knowledge source files.

### Step 2: Project shows available files

When you run `app.py`, it lists all supported files and asks whether you want:

- one file
- multiple files
- all files

This is called file selection.

### Step 3: Selected files are loaded

The file `data_loader.py` reads only the chosen files and converts them into document objects.

For PDFs, it also gets page-wise content, which is why page numbers can later appear in citations.

### Step 4: Text is chunked

Large text is broken into smaller pieces so retrieval becomes better.

### Step 5: Chunks become embeddings

Each chunk becomes a vector using `all-MiniLM-L6-v2`.

### Step 6: Embeddings are stored in FAISS

FAISS keeps the vectors in a searchable structure.

### Step 7: You ask a question

Example:

`What is the objective of the project?`

### Step 8: Your question also becomes an embedding

This allows semantic comparison between the question and the stored chunks.

### Step 9: Most relevant chunks are retrieved

FAISS finds the closest vectors.

### Step 10: Sources are prepared

The system keeps source file names and page numbers with each retrieved chunk.

### Step 11: Groq LLM generates the answer

It gets:

- your question
- top retrieved chunks
- source-aware context

Then it writes the final answer.

### Step 12: Answer and sources are shown

In terminal:

- answer is printed
- source list is printed

In Streamlit:

- answer is shown in the browser
- sources appear below in expandable sections

This is the complete flow.

---

## 32. Deep but Simple Code Explanation

### `src/data_loader.py`

This file has the job of reading files.

Important functions:

- `list_supported_files(data_dir)`
  - scans the folder and returns supported files
- `load_documents_from_files(file_paths)`
  - loads only the selected files
- `load_all_documents(data_dir)`
  - loads all supported files

Important point:

This file now preserves metadata like:

- source file path
- page information for PDFs

That metadata is later used in citations.

### `src/embedding.py`

This file handles two jobs:

1. `chunk_documents()`
   - breaks text into chunks
2. `embed_chunks()`
   - converts chunk text into vectors

Why it matters:

Without this file, semantic search is not possible.

### `src/vectorstore.py`

This file handles FAISS.

Main things it does:

- create index
- add vectors
- save index
- load index
- query index

Very important final change:

It now stores not only chunk text, but also metadata. That is why answers can show source citations.

### `src/search.py`

This is where RAG becomes complete.

Main jobs:

1. load vector store
2. load Groq LLM
3. retrieve similar chunks
4. format source labels like `file.pdf (page 18)`
5. build final prompt
6. call the LLM
7. return answer + sources

This file is the brain of your application.

### `app.py`

This is the terminal app.

Main jobs:

1. show available files
2. let user select files
3. create a unique FAISS folder for that selected file set
4. ensure vector store exists
5. ask questions in terminal
6. print answer and sources

Important point:

It builds a unique vector-store directory for the chosen files. That means different file selections can keep separate indexes.

### `streamlit_app.py`

This is the UI version.

Main jobs:

1. show file multiselect box
2. prepare vector store for selected files
3. accept question from browser input
4. show answer
5. show sources in expanders

Why this matters:

It makes your demo look much more polished.

---

## 33. Terminal vs Streamlit Version

### Terminal Version

Pros:

- simple
- always good as backup
- easy to explain technically

Command:

```powershell
cd "C:\Users\Aman Sharma\Downloads\RAG_Development"
Remove-Item -Recurse -Force .\faiss_store
.\.venv\Scripts\python app.py
```

### Streamlit Version

Pros:

- better appearance
- easier for presentation
- answer and sources look cleaner

Command:

```powershell
cd "C:\Users\Aman Sharma\Downloads\RAG_Development"
.\.venv\Scripts\python -m streamlit run streamlit_app.py
```

Open:

`http://localhost:8501`

Best advice:

- use Streamlit for showing
- keep terminal as backup

---

## 34. What Source Citation Means In Your Project

If the answer is produced from a PDF chunk, the system may show something like:

- `2023A1R042_REPORT(AI_with_CV).pdf (page 18)`

This means:

- answer used text from that PDF
- one supporting chunk came from page 18

Why this is powerful:

- shows the answer is not random
- proves grounding
- makes the project more trustworthy

Short viva answer:

> Source citation means the project shows from which file and page the supporting retrieved content came.

---

## 35. Why We Used Groq Instead of Hugging Face or Ollama For Tomorrow

Your friend may use Hugging Face or Ollama, but for your evaluation your current Groq setup is the best choice.

Why:

1. it is already working
2. it is fast
3. it has lower last-minute risk
4. no need to download heavy local LLM now

When Hugging Face is useful:

- hosted model APIs
- model exploration
- embeddings and transformers ecosystem

When Ollama is useful:

- fully local inference
- no internet dependency after model download

Why not switch now:

- switching on evaluation eve is risky
- current setup already demonstrates RAG well

Short answer if asked:

> I kept Groq because it was already integrated, fast, and reliable for my live mini-project evaluation.

---

## 36. If Teacher Asks “Is This Basic or Advanced?”

Best answer:

> This is an intermediate traditional RAG mini project. It includes document ingestion, chunking, embeddings, FAISS retrieval, Groq-based answer generation, file selection, source citations, and a Streamlit interface. It is more than a basic prototype, but it is not a full production-grade enterprise RAG system.

---

## 37. If Teacher Asks “LangChain or LangGraph?”

Best answer:

> This project is LangChain-style traditional RAG, not LangGraph. It uses loaders and LLM integration in a pipeline form, but it does not use graph-based stateful orchestration.

---

## 38. The Exact Questions You Should Ask In Demo

Use these first:

1. `What is the objective of the project?`
2. `Which model is used in the report?`
3. `What are the selected object categories?`
4. `What are the limitations of the model?`
5. `What is the future scope of the project?`

These are good because your PDF clearly contains these answers.

---

## 39. Final 1-Minute Full Explanation

Memorize this:

> My project is a traditional RAG system for question answering over custom documents. The user uploads files into a local data folder. The system reads those files, splits the content into chunks, converts the chunks into embeddings using a sentence transformer, and stores them in FAISS for semantic retrieval. When the user asks a question, the system retrieves the most relevant chunks and sends them as context to a Groq-hosted LLM, which generates the final answer. In the final version, I also added file selection, source citations with page numbers, and a Streamlit UI for better demonstration.

---

## 40. What You Must Read Before Sleeping

Read these sections from this guide in order:

1. `What is RAG?`
2. `Why RAG is Needed`
3. `Full Project Flow in One Look`
4. `Full End-to-End Working of the Project`
5. `Deep but Simple Code Explanation`
6. `The Exact Questions You Should Ask In Demo`
7. `Final 1-Minute Full Explanation`

If you read those properly, you will understand the whole project at a good level.
