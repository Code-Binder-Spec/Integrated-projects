# Integrated-projects
End-to-end integration pipeline combining async data ingestion, Pydantic validation, dual-storage architecture (SQLite + ChromaDB), and advanced RAG retrieval — hybrid search, reranking, and query decomposition

==== 📂 FOLDER: projects 📦 PROJECT — remotive_job_ai

TYPE: End-to-End Remote Job Search Pipeline with Hybrid RAG Search & Reranking

DESCRIPTION: A Python-based asynchronous pipeline that scrapes live remote job listings from the Remotive public API, stores them in a structured SQLite database and a ChromaDB vector collection, and answers natural language job search queries using Groq's LLaMA 3.3 70B model. User queries are decomposed by the LLM into structured filters (company, salary, job type, location), semantically matched against embedded job postings, then reranked against the structured SQLite data using a custom scoring system — combining vector similarity with exact filter matching for more accurate results than either approach alone.

MAIN FEATURES: ✔ Async scraping of live job listings via aiohttp (Remotive API) ✔ Structured, deduplicated storage using aiosqlite (URL as unique key) ✔ Semantic vector search over job title + description via ChromaDB ✔ LLM-based query decomposition — natural language → structured JSON filters ✔ Custom hybrid reranking system (ScoreBoard) combining vector results with exact-match scoring against structured salary, location, company, and job type data ✔ Robust salary normalization — handles inconsistent real-world formats ($30k-$100k, $14/hr, $31,2k-$52k, OTE prefixes, missing units, etc.) via a custom regex-based extract-then-classify parser, rather than brittle string splitting ✔ Hourly vs. yearly salary classification, since Remotive doesn't label this explicitly in most listings ✔ Context-grounded LLM answers — model is instructed to distinguish real job queries from small talk/test messages before answering, and never fabricates matches outside the retrieved context ✔ Modular file structure — scraping, salary parsing, scoring, and data models are fully separated from orchestration logic ✔ Environment variable based API key management (.env) ✔ Simple terminal-based chat loop with exit command

DATABASE:

jobdata.db — SQLite (structured job fields: title, company, salary_min/max, salary_type, job_type, location, publication_date, url as UNIQUE key)
job.db — ChromaDB persistent client (semantic embeddings of job title + description, metadata-tagged with source URL)

PROJECT STRUCTURE: remotive_job_ai/ ├── main.py # Orchestration entry point (run_pipeline) ├── models.py # Pydantic data model (JobPosting) ├── scraper.py # Remotive API fetching + parsing ├── salary.py # Regex-based salary normalization & classification ├── scoring.py # ScoreBoard hybrid reranking system ├── other_components.py # DB setup, Chroma helpers, Groq call wrapper └── .env # GROQ_API_KEY (not committed)

LEARNING FOCUS:

Async Python — aiohttp, aiosqlite, coroutine design across module boundaries
Vector database persistence and semantic search with ChromaDB
Hybrid retrieval — combining embedding similarity with structured filter scoring for more precise reranking than vector search alone
LLM-based structured extraction (query → JSON) and prompt design for intent classification and hallucination defense
Regex-based data normalization for messy, inconsistent real-world text
Object mutation and state management across async function boundaries (e.g. avoiding shared mutable state bugs in scoring logic)
Modular architecture — separating orchestration from business logic across files with clear single responsibilities
Secure API key handling with environment variables

KEY DESIGN DECISIONS:

URL used as the deduplication key across both SQLite and Chroma, since it's the only guaranteed-unique field in Remotive's listings.
Title + description combined as the embedded text in Chroma, with URL stored as metadata — keeps semantic search broad while allowing exact lookups back to structured data.
Salary parsing rebuilt from manual string-splitting (fragile against spacing/format inconsistencies) to a regex extract-then-classify approach, after real Remotive data exposed edge cases like ambiguous decimal commas and inconsistent "/hr" spacing.
Hourly vs. yearly (not "monthly") classification, based on the finding that Remotive explicitly labels hourly rates but leaves yearly salaries unmarked by convention — monthly figures are rare enough not to warrant a separate default guess.
