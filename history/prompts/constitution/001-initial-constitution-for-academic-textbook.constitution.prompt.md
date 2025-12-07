---
id: 001
title: Initial Constitution for Academic Textbook
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: /sp.constitution
labels: ["governance", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None
---

## Prompt

I am creating a full AI/Spec-Driven textbook project for a hackathon.
Use this prompt to establish the complete constitution for the entire workflow, ensuring accuracy, rigor, and reproducibility.

---------------------------------------------------------
📘 PROJECT OVERVIEW
Create an academic textbook using **Docusaurus**, deployed on **GitHub Pages**, produced through h labs
- Avoid:
  - Blogs without citations
  - Non-expert opinions
  - AI-generated claims without sources

---------------------------------------------------------
🧪 TEXT QUALITY REQUIREMENTS
- Writing level: **Flesch-Kincaid Grade 10–12**
- Tone: academic, precise, neutral
- Explanations must be clear and unambiguous
- Include definitions when introducing technical terms

---------------------------------------------------------
📦 OUTPUT FORMAT REQUIREMENTS
- **Spec-Kit Plus** and **Claude Code**.
The book will cover: **Physical AI & Humanoid Robotics** (topic placeholder – final topic may change later).
This constitution defines all standards the agent must follow during writing, verification, formatting, and output.

---------------------------------------------------------
📌 CORE PRINCIPLES
1. **Accuracy through primary-source verification**
2. **Clarity for an academic audience** (computer science/engineering students)
3. **Reproducibility** – all claims must be traceable
4. **Rigor** – peer-reviewed and scholarly sources preferred
5. **Zero plagiarism tolerance**

---------------------------------------------------------
📑 WRITING & SOURCE STANDARDS
- All factual claims must include citations.
- Citation style: **APA**
- Minimum sources: **15**, with **50% peer-reviewed**.
- Acceptable sources:
  - Peer-reviewed journals
  - Academic books
  - University publications
  - Conference papers
  - Reputable robotics/AI researcTotal word count: **5,000–7,000 words**
- Must generate:
  1. Structured Markdown compatible with **Docusaurus**
  2. A **PDF version** with embedded APA citations
- Internal structure:
  - Title Page
  - Preface
  - Chapter organization
  - Summary sections
  - References section (APA format)

---------------------------------------------------------
🛠 PROCESS REQUIREMENTS
- All claims must be **verified** before inclusion
- Plagiarism check must ensure **0% similarity**
- Agent should self-audit for:
  - Broken citations
  - Unsupported claims
  - Missing references
  - Incorrect formatting
- Must pass a final **fact-checking review**

---------------------------------------------------------
🎯 SUCCESS CRITERIA
- All statements have traceable references
- At least 15 scholarly sources included
- Zero plagiarism detected
- Full clarity at Grade 10–12 reading level
- Output deployable directly to **Docusaurus + GitHub Pages**
- All specs validated by Spec-Kit Plus

---------------------------------------------------------

Use this constitution to guide all future work, planning, drafting, verification, and generation for the textbook project.

## Response snapshot

New Constitution Version: 1.0.0 (Initial creation)

Files flagged for manual follow-up:
*   .specify/templates/plan-template.md: Requires updates to align "Constitution Check" with new principles.
*   .specify/templates/spec-template.md: Requires updates to ensure spec creation fully incorporates new constitution principles (e.g., explicit checks for citation, verification, plagiarism).
*   .specify/templates/tasks-template.md: Requires updates to ensure task categorization reflects new or removed principle-driven task types (e.g., explicit tasks for verification and plagiarism checks).

Suggested commit message:
docs: Initial constitution for Academic textbook v1.0.0 (principles, quality, and output formats defined)

## Outcome

- ✅ Impact: Created the initial project constitution.
- 🧪 Tests: None (documentation task).
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: User will review the constitution and initiate further spec-driven development.
- 🧠 Reflection: Successfully created the constitution by extracting requirements from the user prompt and populating the template. The consistency check identified templates requiring follow-up updates, which are noted in the Sync Impact Report.

## Evaluation notes (flywheel)

- Failure modes observed: Bash script for PHR creation failed, successfully fell back to agent-native tools.
- Graders run and results (PASS/FAIL): None.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
