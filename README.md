# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system provides a unified study companion for the UCF Foundation Exam (FE), a high-stakes test required to remain in the Computer Science major. The exam rules, past exam structures, topic breakdowns, and study advice are scattered across dozens of archived faculty websites, PDFs, and student-maintained repositories. Official exam policies and grading rubrics are difficult to access, and students must piece together study strategies from multiple fragmented sources. This RAG system aggregates these materials into a searchable tool so students can quickly find exam eligibility rules, topic coverage, code templates, partial-credit rubrics, and peer-validated study strategies.

---

## Demo Video

[Watch demo video](./UCFDemo.mp4)

---

## Document Sources

| #   | Source                    | Type                            | URL or file path                                                                              |
| --- | ------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | Current Students Rules    | Official rules document         | `documents/current_students_rules.txt`                                                        |
| 2   | Foundation Exam Info      | Official exam structure PDF     | `http://www.cs.ucf.edu/~dmarino/ucf/transparency/cop3502/lec/FoundationExamInfo.pdf`          |
| 3   | Past Exams Index          | Official exam overview page     | `https://www.cs.ucf.edu/registration/exm/`                                                    |
| 4   | COP3502 Syllabus          | Course syllabus with FE context | `https://www.cs.ucf.edu/courses/cop3502/spr2022/COP3502-Sec12-Syllabus-Spr22.pdf`             |
| 5   | Nick1052 COP3502C README  | UCF Fall 2021 student summary   | `https://raw.githubusercontent.com/Nick1052/COP3502C/master/README.md`                        |
| 6   | VijayStroup ucf-fe README | UCF student FE prep app         | `https://raw.githubusercontent.com/VijayStroup/ucf-fe/master/README.md`                       |
| 7   | Reddit FE Advice          | Student advice from r/ucf       | `documents/reddit_fe_advice.txt`                                                              |
| 8   | JustinHawtree FE Academy  | KnightHacks FE prep project     | `https://raw.githubusercontent.com/JustinHawtree/FE_Academy_KnightHacks2020/master/README.md` |
| 9   | FEPrep README             | Official FEPrep platform        | `https://raw.githubusercontent.com/MewingCentral/FEPrep/main/README.md`                       |
| 10  | RateMyCourses COP3502C    | Student course reviews          | `documents/ratemycourses.txt`                                                                 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 1500 characters

**Overlap:** 300 characters

**Why these choices fit your documents:** Our documents have Markdown headers, exam policies, and syllabus rules where context matters. Smaller chunks (like 500 chars) would split important stuff apart — you'd get a chunk with "Section A: Recursion" but the actual list of recursion topics would be in the next chunk. 1500 characters keeps complete thoughts together. The 300-character overlap bridges chunk boundaries so key terms don't get lost.

**Final chunk count:** ~850 chunks (across all 10 documents after preprocessing)

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `sentence-transformers/all-MiniLM-L6-v2` (runs locally)

**Production tradeoff reflection:** This model is fast and free — perfect for a prototype. But the tradeoff is accuracy on technical CS concepts. The Foundation Exam is heavy on algorithms, recursion, and data structures, which need a smarter embedding model like `text-embedding-3-large` to really understand. In production, we'd swap this out and accept the API costs in exchange for better retrieval on algorithm questions.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** "You are a UCF Foundation Exam advisor. Answer only using the provided exam documents. If the answer isn't in the documents, say 'I don't have that information' instead of making it up."

**How source attribution is surfaced in the response:** After each answer, the system cites which document it came from (e.g., "Source: foundation_exam_info.txt"). This lets students verify answers directly in the official materials.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                                                                               | Expected answer                                                                                                                                      | System response (summarized)                                                                                                                                                      | Retrieval quality | Response accuracy  |
| --- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------ |
| 1   | What are the first steps a student should take when reading Foundation Exam questions?                 | Read ALL questions by 30-min mark; categorize into: (a) I know this & it's quick, (b) I know this but it's lengthy, (c) I'm not sure how to do this. | Correctly identified the 3-category classification approach and the 30-minute timing constraint. Also noted to solve only category (a) questions first on the initial pass.       | Relevant          | Accurate           |
| 2   | If I pass COP 3502 and skip the next available Foundation Exam, what happens to my eligibility window? | If you skip an eligible exam, your eligibility is NOT extended — you lose one of three allowed attempts within the one-year window.                  | Confirmed eligibility is NOT extended and cited multiple sources (foundation_exam_info.txt and cop3502_syllabus.txt). Explained that you lose one of your eligible attempts.      | Relevant          | Accurate           |
| 3   | What is the official passing mark for the Foundation Exam?                                             | The passing mark is 60%, though the exam coordinator reserves the right to move this line.                                                           | Stated the mark is "usually set around 60%" but provided additional context that past exams have used 50%, 55%, 60%, 65%, and 70% depending on score distribution and difficulty. | Relevant          | Partially accurate |
| 4   | How many hours per week should students in COP 3502 expect to spend on the course outside of class?    | The average student should expect 12 hours per week outside of class.                                                                                | Correctly stated "the average student should expect to spend 12 hours a week on the course" and cited cop3502_syllabus.txt.                                                       | Relevant          | Accurate           |
| 5   | What do students say is the biggest challenge when studying for the Foundation Exam?                   | Dynamic memory allocation, recursion, and linked list implementations are frequently mentioned as the most difficult topics.                         | System responded "I don't have enough information on that" and stated that provided sources do not mention student discussions of the biggest challenge.                          | Off-target        | Inaccurate         |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What do students say is the biggest challenge when studying for the Foundation Exam?"

**What the system returned:** "I don't have enough information on that. According to the provided sources (foundation_exam_info.txt and vijaystroup_ucf-fe.txt), there is no mention of students discussing the biggest challenge when studying for the Foundation Exam."

**Root cause (tied to a specific pipeline stage):** The embedding model (all-MiniLM-L6-v2) failed during the retrieval stage. The relevant information exists in the corpus — reddit_fe_advice.txt mentions "dynamic memory allocation" (line 3) and "recursive problem" (line 70), while ratemycourses_cop3502c.txt explicitly lists "linked list, DMA, binary,etc..." (line 30) and describes heavy workload around data structures. However, the embeddings for the query "biggest challenge when studying" did not semantically match these fragmented student discussion snippets. The students don't use the phrase "biggest challenge" directly; instead they mention "weak subjects," "things I had no clue on," and specific topics in passing. The general-purpose embedding model lacks the semantic depth to connect colloquial student language ("stuff that kicks you in the behind," "absolute murder") with technical terminology ("dynamic memory allocation," "recursion," "linked lists").

**What you would change to fix it:** Use a domain-specific or code-aware embedding model (e.g., OpenAI's `text-embedding-3-large`, Voyage AI's `voyage-code-2`, or a fine-tuned embedding trained on CS education materials). Alternatively, preprocess student reviews to explicitly tag difficult topics mentioned, or reduce chunk size to 800–1000 characters so that topic names ("recursion," "DMA") appear more frequently per chunk, increasing embedding density and retrieval likelihood.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The chunking strategy section was super helpful — it explained exactly why 1500 characters mattered for this domain. I realized mid-implementation that smaller chunks were splitting exam rules from their context (like breaking a policy header away from the actual rule), making retrieval inaccurate. The spec gave me confidence to stick with the larger chunk size.

**One way your implementation diverged from the spec, and why:** I initially planned top-3 retrieval, but after testing I dropped it to top-2 because the third chunk often introduced noise from unrelated student reviews. The strategy stayed the same (semantic search), but the k parameter got tighter to match the actual quality of results from this domain.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_ My chunking strategy from planning.md and a list of all 10 document sources (URLs and local files). Asked Claude to write a script that fetches documents, extracts text, and chunks them with the specified parameters.
- _What it produced:_ A Python script using LangChain's RecursiveCharacterTextSplitter that handled plaintext URLs with requests, but didn't account for PDF files.
- _What I changed or overrode:_ Added conditional logic to detect PDF URLs and use pdfplumber for extraction instead. Also tested the actual chunk output and adjusted the separator from `\n\n` to just `\n` because the documents had single newlines between paragraphs, which was causing over-splitting.

**Instance 2**

- _What I gave the AI:_ My 5 test questions from planning.md with expected answers. Asked Claude to generate a system prompt that would make the LLM stick to the retrieved chunks and cite sources.
- _What it produced:_ A prompt template that said "Use only the provided context" but still allowed the LLM to answer if retrieval came up empty.
- _What I changed or overrode:_ Rewrote it to be stricter: "If the answer is not in the provided documents, say 'I don't have that information.'" This forced the system to be honest about gaps instead of hallucinating, which was critical for a study tool where wrong answers are worse than no answer.
