# The Unofficial Guide — Stevens CS Professors

> Ask plain-language questions about Stevens Institute of Technology CS professors and get grounded, cited answers drawn from real Rate My Professors reviews.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Domain

**Stevens Institute of Technology — CS Professor Reviews**

Stevens CS students accumulate a body of knowledge about professors that never appears in any official source. The faculty directory tells you a professor's research interests and office hours — it does not tell you whether they curve, whether their online section is worth taking, or whether they actually show up to class. That knowledge lives on Rate My Professors and in word-of-mouth between students.

This system makes that knowledge searchable. A student can ask "Does Professor Kim curve?" or "Who gives the most useful feedback in the CS department?" and get a grounded, cited answer in seconds — without hunting through Rate My Professors page by page.

**Why it's hard to find otherwise:** RMP reviews are fragmented across individual professor pages, require knowing exact names (students often use nicknames), and offer no way to compare across professors. This system retrieves and synthesizes across all collected reviews at once.

---

## Document Sources

12 documents collected from [Rate My Professors](https://www.ratemyprofessors.com/school/982) (Stevens Institute of Technology, school ID 982). Each document covers one professor: metadata (rating, difficulty, would-take-again %) and 5–7 individual student reviews with course numbers and dates.

| File | Professor | Courses | RMP Rating | Source URL |
|------|-----------|---------|------------|------------|
| `prof_samuel_kim_rmp.txt` | Samuel Kim | CS561, CS562 | 3.4/5 | [ratemyprofessors.com/professor/1083039](https://www.ratemyprofessors.com/professor/1083039) |
| `prof_tian_han_rmp.txt` | Tian Han | CS583, CS559 | 4.2/5 | [ratemyprofessors.com/professor/2531256](https://www.ratemyprofessors.com/professor/2531256) |
| `prof_shudong_hao_rmp.txt` | Shudong Hao | CS382, CS392 | 4.1/5 | [ratemyprofessors.com/professor/2757871](https://www.ratemyprofessors.com/professor/2757871) |
| `prof_david_klappholz_rmp.txt` | David Klappholz | CS574, CS423, CS561 | 1.5/5 | [ratemyprofessors.com/professor/405308](https://www.ratemyprofessors.com/professor/405308) |
| `prof_samantha_kleinberg_rmp.txt` | Samantha Kleinberg | CS544, CS582 | 1.6/5 | [ratemyprofessors.com/professor/1974645](https://www.ratemyprofessors.com/professor/1974645) |
| `prof_igor_faynberg_rmp.txt` | Igor Faynberg | CS524 | 3.3/5 | [ratemyprofessors.com/professor/1979261](https://www.ratemyprofessors.com/professor/1979261) |
| `prof_philippe_meunier_rmp.txt` | Philippe Meunier | CS385 | 4.5/5 | [ratemyprofessors.com/professor/2729187](https://www.ratemyprofessors.com/professor/2729187) |
| `prof_eduardo_bonelli_rmp.txt` | Eduardo Bonelli | CS496, CS511 | 4.2/5 | [ratemyprofessors.com/professor/2113255](https://www.ratemyprofessors.com/professor/2113255) |
| `prof_nikos_triandopoulos_rmp.txt` | Nikos Triandopoulos | CS579, CS396, CS101 | 1.7/5 | [ratemyprofessors.com/professor/2348868](https://www.ratemyprofessors.com/professor/2348868) |
| `prof_dominic_duggan_rmp.txt` | Dominic Duggan | CS522, CS526, CS549 | 2.1/5 | [ratemyprofessors.com/professor/528591](https://www.ratemyprofessors.com/professor/528591) |
| `prof_jacek_ossowski_rmp.txt` | Jacek Ossowski | CS334, CS135 | 3.7/5 | [ratemyprofessors.com/professor/2892587](https://www.ratemyprofessors.com/professor/2892587) |
| `prof_sandeep_bhatt_rmp.txt` | Sandeep Bhatt | CS511, CS546 | 3.0/5 | [ratemyprofessors.com/professor/2233896](https://www.ratemyprofessors.com/professor/2233896) |

All documents are stored in `documents/` and auto-ingested at server startup.

---

## Chunking Strategy

**Chunk size:** 600 characters | **Overlap:** 80 characters | **Splitter:** `RecursiveCharacterTextSplitter` with separators `["\n\n", "\n", ". ", " ", ""]`

**Reasoning:** Each professor document contains short review entries (50–300 characters each), separated by blank lines. With 600-character chunks and recursive splitting on `\n\n` first, each chunk naturally groups 2–4 reviews from the same professor. This gives the embedding model enough semantic content per chunk to represent a coherent opinion, while keeping chunks specific enough that a query about grading policy won't retrieve a chunk dominated by comments about lecture style.

The 80-character overlap ensures that a review split at a boundary carries the professor's name (which appears in the header and is referenced throughout) into the adjacent chunk, preserving retrievability.

**Why not smaller (200 chars):** A single review fragment like "grades strictly but fairly" has no named entity — the embedding cannot anchor the meaning and retrieval becomes unreliable.

**Why not larger (2000 chars):** Chunks spanning entire sections become too general; almost any CS-adjacent query matches them, diluting the signal.

After ingestion, total chunk counts per document ranged from 5 to 10 chunks, for a corpus of ~85 chunks across all 12 files.

### Sample Chunks

**Sample 1** — `prof_samuel_kim_rmp.txt` (chunk 2)
```
Professor: Samuel Kim
Department: Computer Science
Institution: Stevens Institute of Technology
Source: Rate My Professors
Overall Rating: 3.4 / 5.0  |  Difficulty: 3.7 / 5.0  |  Would Take Again: 44%
Courses Taught: CS561 (Database Management Systems), CS562
```
*Self-contained: establishes professor identity and statistics — anchor for all Kim-related queries.*

**Sample 2** — `prof_samuel_kim_rmp.txt` (chunk 5)
```
Course: CS561 | Date: May 2, 2024 | Quality: 4/5 | Difficulty: 3/5 | Grade: A
"Good professor overall. The exams are paper-based and closed book, so make sure you
memorize key query syntax. He does curve at the end. Not the most exciting lectures
but the material is covered thoroughly."
```
*Self-contained: answers a specific query about grading and exam format.*

**Sample 3** — `prof_tian_han_rmp.txt` (chunk 4)
```
Course: CS583 | Date: April 21, 2024 | Quality: 3/5 | Difficulty: 4/5
"Lectures are good and recorded, which I appreciated. Homeworks are not too long but
don't really prepare you for exams at all — there's a big gap between HW difficulty
and exam difficulty. Instructions are not always clear."
```
*Self-contained: directly answers a question about exam vs. homework difficulty for CS583.*

**Sample 4** — `prof_philippe_meunier_rmp.txt` (chunk 1)
```
--- STUDENT REVIEWS ---
Course: CS385 | Date: September 5, 2025 | Quality: 4/5 | Difficulty: 4/5 | Grade: B+
"DO NOT CHEAT. He is very serious about academic integrity and will report you.
Do the homework yourself and you will be fine. Lectures are solid and the homeworks
prepare you well for the exams if you actually do them."
```
*Self-contained: directly answers a query about academic integrity enforcement.*

**Sample 5** — `prof_nikos_triandopoulos_rmp.txt` (chunk 3)
```
Course: CS579 | Date: August 24, 2025 | Quality: 1/5 | Difficulty: 1/5
"This professor is exceptionally difficult to work with. He never shows up to class on
time or at all. He always reschedules office hours and meetings at the last minute.
He is extremely slow at grading — assignments sit ungraded for weeks."
```
*Self-contained: answers "what is the main criticism of Triandopoulos?" in one passage.*

**Sample 6** — `prof_samantha_kleinberg_rmp.txt` (chunk 1)
```
Course: CS544 | Date: May 5, 2026 | Quality: 3/5 | Difficulty: 3/5
"Prof K gives great, engaging lectures and is accessible over email. But, absolutely
no devices allowed in class — no laptops, no tablets, no phones. Assignments are
graded inconsistently: homework is either 0 or 100 with no partial credit. LOTS of
dense reading every week."
```
*Self-contained: answers questions about classroom rules and grading policy.*

---

## Embedding Model

**Model:** `all-MiniLM-L6-v2` via `sentence-transformers`

Runs entirely locally with no API key, no rate limits, and no data leaving the machine. Produces 384-dimensional embeddings optimized for semantic similarity on English sentence-length text. Documents are normalized to unit vectors, and retrieval uses cosine similarity.

**Production tradeoffs:**

| Consideration | all-MiniLM-L6-v2 | Production alternative |
|---|---|---|
| Context window | 256 tokens — sufficient for short reviews | `all-mpnet-base-v2` (512 tokens) for longer documents |
| Multilingual | English-only — misses non-English reviews | `paraphrase-multilingual-MiniLM-L12-v2` for international students |
| Domain specificity | General-purpose | Fine-tuned on student feedback data would improve recall |
| Latency | ~5ms/query on CPU | OpenAI `text-embedding-3-small` is faster at API scale but costs money |
| Privacy | 100% local | Any API-based embedding sends data externally |

For this domain (English short-text reviews), `all-MiniLM-L6-v2` performs well. In a production system with multilingual users or longer source documents, the tradeoffs above would justify a more capable model.

---

## Retrieval Test Results

**Setup:** top-k = 4 chunks, cosine similarity via ChromaDB

### Query 1: "Does Samuel Kim curve grades in CS561?"

Top retrieved chunks (document: `prof_samuel_kim_rmp.txt`):

| Rank | Distance | Chunk excerpt |
|------|----------|---------------|
| 1 | 0.941 | "Kim is knowledgeable but the homework problems are significantly harder than what he covers in lecture…" |
| 2 | 1.102 | Header block: rating 3.4/5, difficulty 3.7/5, courses CS561/CS562 |
| 3 | 1.117 | **"He does curve at the end. Not the most exciting lectures but the material is covered thoroughly."** |
| 4 | 1.254 | "The professor is not too tough since he curved the grades." |

**Why the top chunks are relevant:** Chunks 3 and 4 directly confirm the curving behavior. Chunk 1 is relevant context about the difficulty gap that makes curving meaningful. The answer is present in the retrieved set, though not at rank 1 — the query word "curve" appears in chunk 3, which scores distance 1.117. The embedding model found the header block (chunk 2) slightly more semantically similar to a "CS561 grades" query than the passage about curving, which is a realistic retrieval imprecision.

---

### Query 2: "What do students say about Tian Han's exams vs. homework?"

Top retrieved chunks (document: `prof_tian_han_rmp.txt`):

| Rank | Distance | Chunk excerpt |
|------|----------|---------------|
| 1 | 0.609 | "The homework assignments are straightforward but the midterm came out of nowhere." |
| 2 | 0.987 | "Homeworks are not too long but don't really prepare you for exams at all — there's a big gap between HW difficulty and exam difficulty." |
| 3 | 1.169 | "Great slides, but refuses to use a mic… Lectures are recorded…" |

**Why the top chunks are relevant:** The distance of 0.609 on rank 1 is strong (well below the 0.5–0.6 concern threshold for this corpus). Both rank 1 and rank 2 directly describe the exam/homework difficulty gap from different reviewers. The retrieval is precise and would support a well-grounded LLM response.

---

### Query 3: "What are the main complaints about Nikos Triandopoulos?"

Top retrieved chunks (document: `prof_nikos_triandopoulos_rmp.txt`):

| Rank | Distance | Chunk excerpt |
|------|----------|---------------|
| 1 | 1.213 | "Triandopoulos never showed up for class. The first time we had an in-person lecture was after four weeks…" |
| 2 | 1.354 | Header block: rating 1.7/5, 9% would take again |
| 3 | 1.493 | "He never shows up to class on time or at all. He always reschedules office hours and meetings at the last minute." |

**Why the top chunks are relevant:** All three retrieved passages are directly relevant. Ranks 1 and 3 independently corroborate the same criticism (not attending class), which gives the LLM grounded, multi-source evidence for its answer. The header block (rank 2) adds quantitative context (1.7/5, 9% would take again).

---

## Grounded Generation

**How grounding is enforced:**

The system prompt passed to the LLM is:

```
You are a helpful assistant for Stevens Institute of Technology students.
Answer the question using ONLY the information in the provided context.
If the context does not contain enough information to answer, say
"I don't have enough information on that in the documents."
Always mention which professor or source your answer refers to.

Context:
{context}

Question: {question}
```

The `{context}` slot is filled programmatically with the retrieved chunk text — the LLM never sees anything other than what retrieval returned. Source attribution is reinforced both by the prompt instruction ("always mention which professor") and structurally: the retrieved chunks themselves contain professor names, dates, and course numbers that carry into any grounded response.

**LLM:** Groq `llama-3.3-70b-versatile` (free tier, [console.groq.com](https://console.groq.com)) when `GROQ_API_KEY` is set; fallback to local Ollama otherwise.

---

## Example Responses

### Example 1 — Grounded response with citation

**Query:** "What do students say about Tian Han's exams compared to his homework?"

**System response:**
> Based on student reviews of Professor Tian Han (CS583 — Machine Learning at Stevens), there is a consistent pattern: the homework is considered manageable or easy, but the exams are significantly harder and not well-predicted by the homework. One reviewer wrote: "Homeworks are not too long but don't really prepare you for exams at all — there's a big gap between HW difficulty and exam difficulty." Another noted: "The homework assignments are straightforward but the midterm came out of nowhere." Additionally, because Professor Han does not write his own homeworks, he is unable to help students debug them — students are advised to go to TAs instead.
>
> *Sources: prof_tian_han_rmp.txt (CS583 reviews, Rate My Professors)*

**Source attribution visible in UI:** The source drawer shows the document filename `tian_han` (formatted as `tian_han`) and chunk index for each of the 4 retrieved passages.

---

### Example 2 — Grounded response with citation

**Query:** "Is Philippe Meunier strict about cheating?"

**System response:**
> Yes, multiple student reviews indicate that Philippe Meunier (CS385 — Algorithms and Data Structures) takes academic integrity very seriously. One reviewer wrote: "DO NOT CHEAT. He is very serious about academic integrity and will report you. Do the homework yourself and you will be fine." A second reviewer noted that he is "very quick to suspect cheating without solid evidence" and may initiate honor board proceedings. The consensus is that the course is fair if you do your own work, but there is significant risk if you don't.
>
> *Sources: prof_philippe_meunier_rmp.txt (CS385 reviews, Rate My Professors)*

---

### Example 3 — Out-of-scope refusal

**Query:** "What is the best restaurant near the Stevens campus?"

**System response:**
> I don't have enough information on that in the documents. The available documents cover student reviews of CS professors at Stevens Institute of Technology — they don't include information about restaurants or dining options near campus.

This response demonstrates that the system declines to answer questions outside its document scope rather than generating plausible-sounding information from the LLM's general training knowledge.

---

## Query Interface

**Input field:** A text box labeled "Your question" — accepts free-form natural language questions about Stevens CS professors.

**Output:** Two fields:
- **Answer** (8-line text area) — the LLM's grounded response, streamed token-by-token via Server-Sent Events
- **Retrieved from** (4-line text area) — the source document filenames the answer drew from

Additionally, a **Source Passages drawer** can be opened by clicking any response. It shows the 4 retrieved passages, each labeled with the source filename (e.g., `samuel_kim`) and chunk index.

**Model selector** (top-right): displays available models. When `GROQ_API_KEY` is set, `llama-3.3-70b-versatile` appears first. Ollama models follow if available.

**Document selector** (left sidebar): lists all indexed professor documents with chunk counts. Click to select which document to query.

### Sample interaction transcript

```
User:    Does Professor Kim curve his grades?

System:  [Sources retrieved: prof_samuel_kim_rmp.txt, chunks 3, 5, 6, 2]

         Based on student reviews of Samuel Kim (CS561 — Database Management
         Systems at Stevens), yes — he does curve grades. One reviewer wrote:
         "He does curve at the end. Not the most exciting lectures but the
         material is covered thoroughly." Another noted: "The professor is not
         too tough since he curved the grades." That said, the homework is
         described as significantly harder than lecture content, so the curve
         appears to compensate for the difficulty gap rather than being a
         guaranteed boost.

         Sources: prof_samuel_kim_rmp.txt (Rate My Professors)
```

---

## Evaluation Report

### Test Questions and Results

| # | Question | Expected Answer | System Response | Retrieval | Response |
|---|----------|-----------------|-----------------|-----------|----------|
| 1 | Does Samuel Kim curve grades in CS561? | Yes — multiple reviews confirm curving | Correctly cited two reviews confirming Kim curves; added context about homework difficulty | ✅ Accurate | ✅ Accurate |
| 2 | What do students say about Tian Han's exams vs. homework? | Homework manageable, exams significantly harder | Correctly described the gap; cited "big gap between HW difficulty and exam difficulty"; mentioned TA advice | ✅ Accurate | ✅ Accurate |
| 3 | Is Philippe Meunier strict about academic integrity? | Yes — multiple reviews warn against cheating explicitly | Correctly cited "DO NOT CHEAT" review and honor board mention | ✅ Accurate | ✅ Accurate |
| 4 | Which CS professor in this system has the highest % of students who would take them again? | Philippe Meunier at 87% | **Failure** — see below | ❌ Inaccurate | ❌ Inaccurate |
| 5 | What are the main complaints about Nikos Triandopoulos? | Doesn't show up to class; reschedules constantly | Correctly cited two independent reviews about class absences and rescheduling | ✅ Accurate | ✅ Accurate |

**Overall: 4/5 accurate, 1/5 failure.**

---

### Failure Case Analysis

**Question 4:** "Which CS professor in this system has the highest percentage of students who would take them again?"

**Expected answer:** Philippe Meunier (87% would take again).

**What the system returned:** The system cannot answer this question because each professor's reviews are stored in a separate ChromaDB collection. When a user selects a document and asks a question, retrieval searches only that document's collection. A cross-professor comparison query retrieves passages from one professor's file only — it has no mechanism to look up the would-take-again statistics from all 12 documents simultaneously.

**Why it happened:** The architecture uses per-document ChromaDB collections (one collection per file). This was a deliberate design choice that supports the general use case of "ask a question about this specific document." But it creates a structural limitation for comparative queries that span multiple documents. The system would need a unified index (all chunks in one collection, with source metadata for filtering) or a multi-retrieval step to support cross-professor comparisons.

**What retrieval actually returned:** When the Meunier document was selected and the cross-comparison query was issued, the system returned chunks from Meunier's file about his teaching style — not the would-take-again statistics. The retrieved chunks did not contain the comparison context needed to answer the question correctly.

**Fix:** Merge all professor chunks into a single ChromaDB collection with a `professor` metadata field, then retrieve across all documents. This is a straightforward architectural change that would unblock all cross-professor queries.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Document Collection (offline)                  │
│  Rate My Professors → 12 × .txt files in documents/                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ startup auto-ingest
┌──────────────────────────▼──────────────────────────────────────┐
│                  Ingestion Pipeline (FastAPI startup)            │
│  TextLoader → RecursiveCharacterTextSplitter (600c / 80 overlap) │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Embedding + Vector Store                        │
│  all-MiniLM-L6-v2 (sentence-transformers, local)                │
│  ChromaDB — one collection per document                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ cosine similarity, top-4
┌──────────────────────────▼──────────────────────────────────────┐
│                  Retrieval                                       │
│  Query → embed → ChromaDB similarity search → top-4 chunks      │
│  Source filename attached to each retrieved chunk               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Generation (LLM)                                │
│  Groq: llama-3.3-70b-versatile (free tier, context-only prompt) │
│  Fallback: Ollama local (llama3.2, mistral, etc.)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ streaming SSE tokens
┌──────────────────────────▼──────────────────────────────────────┐
│                  Query Interface                                 │
│  Next.js 14 (App Router, TypeScript, Tailwind)                  │
│  ChatPanel: streaming response + source drawer                  │
│  ModelSelector: Groq first if API key set, then Ollama          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | FastAPI, Uvicorn, Python 3.11 |
| LLM orchestration | LangChain (LCEL) |
| Embeddings | `all-MiniLM-L6-v2` via sentence-transformers (local) |
| Vector store | ChromaDB (persistent) |
| LLM (primary) | Groq `llama-3.3-70b-versatile` (free tier) |
| LLM (fallback) | Ollama (local inference) |
| Text processing | LangChain `TextLoader`, `RecursiveCharacterTextSplitter` |
| Containerization | Docker + Docker Compose |
| CI | GitHub Actions |

---

## Quick Start — Docker

**Prerequisites:** Docker + Docker Compose + a free Groq API key from [console.groq.com](https://console.groq.com)

```bash
# 1. Clone
git clone https://github.com/ichowdhury10/rag-knowledge-assistant.git
cd rag-knowledge-assistant

# 2. Set your Groq API key
echo "GROQ_API_KEY=your_key_here" > backend/.env

# 3. Start all services (documents/ is auto-ingested on first boot)
docker compose up --build

# 4. Open the app
open http://localhost:3000
```

Select any professor document from the sidebar and start asking questions.

If you prefer a local Ollama model instead of Groq:
```bash
# Skip GROQ_API_KEY — just start Ollama and pull a model
ollama pull llama3.2
docker compose up --build
```

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set GROQ_API_KEY and DATA_DIR=../data

uvicorn app.main:app --reload --port 8000
# Auto-ingests documents/ on startup
# API docs: http://localhost:8000/api/docs
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local   # API_URL=http://localhost:8000
npm run dev
# App: http://localhost:3000
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | `""` | Groq API key — enables `llama-3.3-70b-versatile` |
| `DATA_DIR` | `../data` | Path to professor review documents (auto-ingested at startup) |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model (local) |
| `CHUNK_SIZE` | `600` | Characters per chunk |
| `CHUNK_OVERLAP` | `80` | Overlap between adjacent chunks |
| `RETRIEVAL_K` | `4` | Top-k passages retrieved per query |
| `OLLAMA_BASE_URL` | `http://ollama:11434` | Ollama service URL (fallback LLM) |

---

## Spec Reflection

**One way the spec helped:** Writing the chunking strategy section of `planning.md` before touching any code forced a concrete decision about chunk size upfront. Having committed to "600 characters / 80 overlap because reviews are 50–300 characters each," I didn't need to experiment blindly — I could immediately verify whether chunks were self-contained by printing them post-ingestion. This was the most useful part of the spec: it made the verification criteria concrete.

**One way implementation diverged from the spec:** The spec assumed a single unified ChromaDB collection with source metadata for filtering. The existing implementation (inherited from the general-purpose RAG system) uses per-document collections — one ChromaDB collection per uploaded file. I kept this design because it fit the existing upload flow and the UI's document-selector model, but it directly caused the failure on Question 4 (cross-professor comparison). If I were starting from scratch for this domain specifically, I would use a unified collection with a `professor` metadata field from the beginning.

---

## AI Usage

**Instance 1 — Groq LLM integration**

I directed Claude to implement the Groq LLM branch in `_build_chain()` by providing: the current `rag_service.py`, the `config.py` settings, and the requirement to use `ChatGroq` for `llama-3.3-70b-versatile` while falling back to `OllamaLLM` for all other model names. The generated code correctly used `langchain_groq.ChatGroq` with the `api_key` parameter. I overrode one thing: the initial generated code used a global `if GROQ_API_KEY:` check at import time, which would have broken the module for users without a key. I changed it to a lazy check inside `_build_llm()` so the module loads cleanly regardless.

**Instance 2 — Text file ingestion**

I directed Claude to extend `upload_document()` to support `.txt` files alongside PDFs, providing the existing function and the requirement that it use `TextLoader` with UTF-8 encoding. The generated code was correct but added an `UnstructuredFileLoader` import that wasn't needed — I removed it. I also added the `_process_chunks()` helper to attach `filename` metadata to each chunk, which the AI had suggested putting inline but I extracted for clarity.

**Instance 3 — `ingest_data_dir()` function**

I directed Claude to implement a startup ingestion function using the architecture diagram from `planning.md`. The generated function correctly handled deduplication by checking `already_ingested` against `_documents.values()`. I verified the deduplication logic myself and confirmed it correctly skips files that were already in the registry before accepting the output.

---

## Project Structure

```
rag-knowledge-assistant/
├── documents/                            # 12 Stevens CS professor review documents
│   ├── prof_samuel_kim_rmp.txt
│   ├── prof_tian_han_rmp.txt
│   └── ...
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + lifespan auto-ingest
│   │   ├── config.py            # Settings (pydantic-settings, includes GROQ_API_KEY)
│   │   ├── schemas.py           # Pydantic models (SourcePassage includes source field)
│   │   ├── routers/
│   │   │   ├── documents.py     # Upload PDF/TXT, list, delete
│   │   │   ├── chat.py          # Streaming + blocking chat
│   │   │   └── models.py        # Groq models first, then Ollama
│   │   └── services/
│   │       ├── rag_service.py   # Pipeline: ingest → chunk → embed → retrieve → generate
│   │       └── vectorstore.py   # ChromaDB helpers
│   ├── requirements.txt         # Includes langchain-groq, groq
│   └── Dockerfile
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── SourceDrawer.tsx  # Shows source filename per passage
│       │   └── UploadZone.tsx    # Accepts PDF and TXT
│       └── lib/
│           └── types.ts          # SourcePassage includes optional source field
├── scripts/
│   └── ingest_data.py           # Manual ingestion script (server auto-ingests on start)
├── planning.md                  # Written before implementation
├── docker-compose.yml           # Mounts documents/ as read-only volume
└── README.md
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents/upload` | Upload a PDF or TXT file |
| `GET` | `/api/documents/` | List all indexed documents |
| `DELETE` | `/api/documents/{id}` | Remove a document |
| `POST` | `/api/chat/stream` | Stream an answer (SSE) |
| `POST` | `/api/chat/` | Blocking chat endpoint |
| `GET` | `/api/models/` | List available models (Groq first, then Ollama) |
| `GET` | `/api/health` | Health check |

Interactive docs: `http://localhost:8000/api/docs`

---

## License

MIT
