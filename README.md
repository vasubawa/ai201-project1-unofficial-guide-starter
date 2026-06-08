# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system provides a unified study companion for the UCF Foundation Exam (FE), a high-stakes test required to remain in the Computer Science major. The exam rules, past exam structures, topic breakdowns, and study advice are scattered across dozens of archived faculty websites, PDFs, and student-maintained repositories. Official exam policies and grading rubrics are difficult to access, and students must piece together study strategies from multiple fragmented sources. This RAG system aggregates these materials into a searchable tool so students can quickly find exam eligibility rules, topic coverage, code templates, partial-credit rubrics, and peer-validated study strategies.

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

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | -------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   |          |                 |                              |                   |                   |
| 2   |          |                 |                              |                   |                   |
| 3   |          |                 |                              |                   |                   |
| 4   |          |                 |                              |                   |                   |
| 5   |          |                 |                              |                   |                   |

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_

**Instance 2**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_
