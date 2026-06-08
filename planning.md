# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

**UCF Computer Science Foundation Exam (FE) Study Companion**
This system unifies fragmented study materials for the UCF Foundation Exam, a high-stakes test required to stay in the Computer Science major. Official exam rules, past solutions, and professor tips are scattered across dozens of older faculty web pages and PDFs. This RAG system aggregates these resources into a single searchable tool so students can quickly find exam policies, code templates, and partial-credit grading rubrics.

---

## Documents

## Documents

| #   | Source                    | Description                                                              | URL / Location                                                                                |
| --- | ------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 1   | Current Students Rules    | Official FE rules, eligibility, passing line, schedule.                  | `documents/current_students_rules.txt`                                                        |
| 2   | Foundation Exam Info      | Exam structure, 4 sections A-D, 25pts each, topic breakdown.             | `http://www.cs.ucf.edu/~dmarino/ucf/transparency/cop3502/lec/FoundationExamInfo.pdf`          |
| 3   | Past Exams Index          | Overview page describing the exam format and all past exams.             | `https://www.cs.ucf.edu/registration/exm/`                                                    |
| 4   | COP3502 Syllabus          | Topics covered, FE context, study expectations.                          | `https://www.cs.ucf.edu/courses/cop3502/spr2022/COP3502-Sec12-Syllabus-Spr22.pdf`             |
| 5   | Nick1052 COP3502C README  | UCF Fall 2021 student's summary of exactly what COP3502 covers.          | `https://raw.githubusercontent.com/Nick1052/COP3502C/master/README.md`                        |
| 6   | vijaystroup ucf-fe README | UCF student who built an FE prep app, describes the exam directly.       | `https://raw.githubusercontent.com/VijayStroup/ucf-fe/master/README.md`                       |
| 7   | Reddit FE Advice          | Student advice from r/ucf regarding passing the Foundation Exam.         | `documents/reddit_fe_advice.txt`                                                              |
| 8   | JustinHawtree FE Academy  | UCF KnightHacks project built specifically to help students pass the FE. | `https://raw.githubusercontent.com/JustinHawtree/FE_Academy_KnightHacks2020/master/README.md` |
| 9   | FEPrep README             | Official FEPrep platform GitHub repo describing the exam and topics.     | `https://raw.githubusercontent.com/MewingCentral/FEPrep/main/README.md`                       |
| 10  | RateMyCourses COP3502C    | Student reviews mentioning foundation exam prep and difficulty.          | `documents/ratemycourses.txt`                                                                 |

---

## Chunking Strategy

**Chunk size:** 1500 characters.

**Overlap:** 300 characters.

**Reasoning:** Because this corpus includes Markdown headers and syllabus policies, small chunks would split critical context (e.g., breaking a list of FE topics away from its explanation). A 1500-character chunk size ensures that full algorithmic structures and exam rules remain completely intact. The 300-character overlap preserves continuity, ensuring terms or rules introduced at the end of one chunk aren't lost in the next.

---

## Retrieval Approach

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (running locally).

**Top-k:** 3 chunks.

**Production tradeoff reflection:** While all-MiniLM-L6-v2 is perfect for a fast, free local prototype, a production deployment would switch to a code-optimized embedding model like text-embedding-3-large or Voyage AI. The Foundation Exam heavily evaluates algorithm concepts and big-O notation, which require advanced models to achieve high semantic accuracy. The main tradeoffs of this upgrade would be cloud API costs and increased network latency compared to our local model.

---

## Evaluation Plan

| #   | Question                                                                                                                               | Expected answer                                                                                                                 |
| --- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | What are the first steps a student should take when reading Foundation Exam questions?                                                  | Read ALL the questions by the 30 minute mark. On the first pass, identify each question into categories: (a) I know how to do this and it's fairly quick, (b) I know how to do this but it's lengthy, (c) I am not sure how to do this. |
| 2   | If I pass COP 3502 and skip the next available Foundation Exam, what happens to my eligibility window?                                  | If you choose not to attend an exam you are eligible for, your eligibility is NOT extended. You lose one of your three allowed attempts within the one-year window. |
| 3   | What is the official passing mark for the Foundation Exam?                                                                              | The passing mark is 60%. However, the exam coordinator reserves the right to move this passing line for any reason.             |
| 4   | How many hours per week should students in COP 3502 expect to spend on the course outside of class?                                    | The average student should expect to spend 12 hours per week on the course outside of class.                                   |
| 5   | What do students say is the biggest challenge when studying for the Foundation Exam?                                                   | Dynamic memory allocation, recursion, and linked list implementations are frequently mentioned as difficult topics that require focused practice. |

---

## Anticipated Challenges

1. **GitHub Markdown Noise:** Some of the GitHub readmes might contain standard boilerplate (like "How to install node.js" for the FE Prep apps) that dilutes the actual Foundation Exam advice. If the AI retrieves a chunk about installing an app instead of studying for the exam, it could lead to hallucinations.
2. **Context Loss on Chunking:** If a document has a header that says "Section A: CS1 Topics" and the chunk splits halfway through the list, the second chunk might just contain concepts like "Sorting" without the context that it belongs to Section A, making retrieval inaccurate.

---

## Architecture

```text
[ Raw Data: URLs, PDFs, Local Text ]
           │
           ▼
[ Ingestion Pipeline ] ── (Libraries: pdfplumber, requests, BeautifulSoup)
   Extract text & clean whitespace
           │
           ▼
[ Chunking Strategy ] ── (Library: LangChain RecursiveCharacterTextSplitter)
   Split into 1500-character chunks with 300-character overlap
           │
           ▼
[ Embedding Model ] ── (Library: sentence-transformers all-MiniLM-L6-v2)
   Convert text chunks to dense vector embeddings
           │
           ▼
[ Vector Database ] ── (Library: ChromaDB)
   Store chunks + metadata + embeddings locally
           │
           ▼
[ Retrieval ] ── (Semantic Search via ChromaDB)
   Query embedded ──────> Return Top-K (3) relevant chunks
           │
           ▼
[ Generation ] ── (Library: Groq API with llama-3.3-70b-versatile)
   Prompt: "Answer using only the retrieved chunks..."
           │
           ▼
[ Final Output to User ]
```
