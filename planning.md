# planning.md — The Unofficial Guide: Stevens CS Professors

> Written before implementation, per project requirements.
> Last updated: 2026-06-10

---

## Domain

**Stevens Institute of Technology — Computer Science Professor Reviews**

Stevens CS students generate a large body of informal knowledge about professors that never appears in official channels. The official faculty directory lists names, research interests, and office hours. It does not tell you whether a professor curves, how hard their exams are relative to their homework, whether they actually show up to class, or whether their online section is equivalent to in-person. That knowledge lives on Rate My Professors, Reddit's r/Stevens, and in word-of-mouth between students.

This system makes that knowledge searchable. A student asking "Does Professor Kim curve?" or "Which professor should I take for Algorithms?" should get a grounded, cited answer drawn from real student reviews — not generic advice or hallucinated statistics.

---

## Documents

12 source documents, all collected from Rate My Professors (ratemyprofessors.com):

| File | Professor | Courses | RMP Rating |
|------|-----------|---------|------------|
| `prof_samuel_kim_rmp.txt` | Samuel Kim | CS561, CS562 | 3.4/5 |
| `prof_tian_han_rmp.txt` | Tian Han | CS583, CS559 | 4.2/5 |
| `prof_shudong_hao_rmp.txt` | Shudong Hao | CS382, CS392 | 4.1/5 |
| `prof_david_klappholz_rmp.txt` | David Klappholz | CS574, CS423, CS561 | 1.5/5 |
| `prof_samantha_kleinberg_rmp.txt` | Samantha Kleinberg | CS544, CS582 | 1.6/5 |
| `prof_igor_faynberg_rmp.txt` | Igor Faynberg | CS524 | 3.3/5 |
| `prof_philippe_meunier_rmp.txt` | Philippe Meunier | CS385 | 4.5/5 |
| `prof_eduardo_bonelli_rmp.txt` | Eduardo Bonelli | CS496, CS511 | 4.2/5 |
| `prof_nikos_triandopoulos_rmp.txt` | Nikos Triandopoulos | CS579, CS396, CS101 | 1.7/5 |
| `prof_dominic_duggan_rmp.txt` | Dominic Duggan | CS522, CS526, CS549 | 2.1/5 |
| `prof_jacek_ossowski_rmp.txt` | Jacek Ossowski | CS334, CS135 | 3.7/5 |
| `prof_sandeep_bhatt_rmp.txt` | Sandeep Bhatt | CS511, CS546 | 3.0/5 |

Each file contains: professor metadata (name, rating, difficulty, would-take-again %), a list of courses they teach, and 5–7 individual student reviews with course number, date, quality rating, and review text.

**Why these sources are hard to find through official channels:** The Stevens course catalog lists professors but not opinions about them. Rate My Professors is fragmented — students need to look up each professor individually, remember their exact name (students often refer to "Big P" or "Prof K"), and filter noise from off-topic reviews. This system lets a student ask a natural-language question and get a synthesized, cited answer in seconds.

---

## Chunking Strategy

**Chunk size:** 600 characters  
**Overlap:** 80 characters  
**Splitter:** `RecursiveCharacterTextSplitter` with separators `["\n\n", "\n", ". ", " ", ""]`

**Reasoning:**

Professor reviews are short, opinion-dense texts — typically 50–300 characters per individual review. A 600-character chunk will capture 2–4 reviews per chunk, which is the right granularity: enough context for the embedding to represent a coherent opinion about one professor, but not so large that a chunk about Professor A's grading policy gets mixed with unrelated content about Professor B.

The document format I used structures each professor's data as:
1. A header block (professor name, rating, courses) — ~200 characters
2. Individual reviews separated by blank lines — ~150–300 characters each

With 600-character chunks and recursive splitting on `\n\n` first, most chunks will naturally group 2–3 reviews from the same professor. The 80-character overlap ensures that a review split across a chunk boundary has enough of the previous context (typically the prior review's sentiment or the professor's name from the header) to remain retrievable.

**What would bad chunking look like here:**
- *Too small (200 chars):* A single review fragment without the professor's name — "grades strictly but fairly" — is almost unsearchable. The embedding has no named entity to anchor the semantic meaning.
- *Too large (2000 chars):* A chunk spanning the entire professor file would match almost any query about that professor, but the retrieved chunk would be too diluted for the LLM to extract a precise answer. All retrieval would surface the same few large blobs.

**Why 600 is the sweet spot:** At 600 characters with `\n\n` splitting, each chunk contains the professor's name (from the header, which recurs in the file) and 2–3 focused reviews. The chunk is specific enough for precise retrieval but rich enough to support a complete answer.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`  
**Vector store:** ChromaDB (local persistent)  
**Top-k:** 4 chunks per query  
**Similarity metric:** Cosine similarity (default in ChromaDB + `normalize_embeddings=True`)

**Why all-MiniLM-L6-v2:** It runs entirely locally with no API key or rate limits, making it ideal for a development system and demo that can't depend on external availability. It produces 384-dimensional embeddings that capture semantic similarity well for English text — good enough that "curves grades" and "grade curve" will be close in embedding space, which matters for review-style queries.

**Production tradeoffs I would consider:**
- *Context length:* all-MiniLM-L6-v2 is capped at 256 tokens. For longer documents (syllabi, housing guides), `all-mpnet-base-v2` (768-dim, 512-token window) would be better.
- *Multilingual support:* Stevens has a large international student population. A multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would handle non-English queries, though it is slower.
- *Domain-specific accuracy:* A model fine-tuned on student feedback data (none publicly available for this domain) would likely outperform a general-purpose model on queries about grading and teaching style.
- *API vs. local:* OpenAI's `text-embedding-3-small` or Cohere's `embed-v3` would give higher quality but at per-token cost and with data leaving the machine.

**Why top-k = 4:** Four chunks balance coverage vs. context dilution. With ~600-char chunks at 4-per-query, the LLM receives ~2400 characters of grounded context — enough for a nuanced answer without overwhelming the prompt. At k=2, edge-case queries (a professor with sparse reviews) may miss the relevant passage. At k=8, loosely related reviews from other professors can dilute the answer.

---

## Evaluation Plan

Five test questions with expected correct answers:

| # | Question | Expected Answer |
|---|----------|-----------------|
| 1 | Does Samuel Kim curve grades in CS561? | Yes — multiple reviews mention grading curves; one reviewer said "the professor is not too tough since he curved the grades" |
| 2 | What do students say about Tian Han's exams vs. homework? | Homework is manageable but exams are significantly harder and not well-predicted by the homework; one reviewer noted "homeworks don't really prepare for exams almost at all" |
| 3 | Is Philippe Meunier strict about academic integrity? | Yes — multiple reviews explicitly warn against cheating; one review says "DONT CHEAT, do homework and pass" |
| 4 | Which professor in this index has the highest percentage of students who would take them again? | Philippe Meunier at 87% would-take-again |
| 5 | What is the main criticism of Nikos Triandopoulos? | He frequently doesn't show up to class; multiple reviews cite cancelled classes, last-minute rescheduling, and a commute from Boston causing frequent online switches |

---

## Anticipated Challenges

**1. Nickname / alias mismatch in retrieval**  
Students often refer to professors by nickname ("Big P" for Meunier, "Prof K" for Kleinberg). If a user queries "who is Big P?" the embedding may not connect this to Meunier's file unless the nickname appears in the retrieved chunk. Mitigation: include nicknames in the document text where they appear in reviews.

**2. Sparse review coverage for some professors**  
Some professors have fewer reviews. With k=4 retrieval and only 6 reviews in the file, some queries may retrieve chunks from the wrong professor if the semantic distance is close. This is a genuine failure mode to document in the evaluation.

**3. Contradictory reviews**  
Some professors (Faynberg, Duggan) have sharply divided reviews — some students rate them 5/5, others 1/5. The LLM must represent this contradiction honestly rather than averaging it into a false consensus. The prompt instructs it to answer from retrieved context only, which should surface the split opinion.

**4. Cross-professor queries**  
A question like "which professor gives the most useful feedback?" requires comparing across multiple professor documents. Since the system retrieves from one document at a time (per the current architecture), cross-professor comparisons may fail. This is a known limitation of the single-collection-per-document design.

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
│  Sources metadata attached to each retrieved chunk               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Generation (LLM)                                │
│  Groq: llama-3.3-70b-versatile (free tier)                      │
│  Fallback: Ollama local (llama3.2, mistral, etc.)               │
│  Prompt: answer from context only + cite sources                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ streaming SSE tokens
┌──────────────────────────▼──────────────────────────────────────┐
│                  Query Interface                                 │
│  Next.js 14 (App Router, TypeScript, Tailwind)                  │
│  Sidebar: document selector                                     │
│  ChatPanel: streaming response + source drawer                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## AI Tool Plan

I plan to use AI tools (Claude) for the following specific implementation tasks:

| Component | Input to AI | Expected Output |
|-----------|-------------|-----------------|
| Groq LLM integration | `rag_service.py` + `config.py` + requirement to support `llama-3.3-70b-versatile` | Modified `_build_llm()` function that conditionally initializes `ChatGroq` vs `OllamaLLM` based on model name and API key availability |
| `.txt` file ingestion | Current `upload_document()` + requirement to support `.txt` in addition to `.pdf` | Extended function using `TextLoader` with the same chunking pipeline |
| `ingest_data_dir()` startup function | Architecture diagram (documents/ → TextLoader → ChromaDB) + deduplication requirement | `ingest_data_dir()` function that skips already-indexed files |
| Evaluation script | 5 test questions from evaluation plan + response format | Script that runs each question and formats results as a markdown table |

For each generated output, I will: verify that the code matches the spec (correct model names, correct file extension checks, correct metadata fields), test it against the live system, and document any divergence in the spec reflection section of the README.
