# 🤖📘 Physical AI & Humanoid Robotics — AI‑Native Textbook

This repository contains a **fully completed Hackathon I project**: an **AI‑Native Textbook for Teaching Physical AI & Humanoid Robotics**, built exactly according to the official Panaversity Hackathon requirements.

All required features **have been implemented and are working correctly**.

---

## 🏆 Hackathon Context

**Hackathon I: Create a Textbook for Teaching Physical AI & Humanoid Robotics**

The future of work will be a collaboration between humans, intelligent agents, and robots. This project contributes to that future by delivering an **AI‑Native, interactive, and personalized learning platform** for Physical AI & Humanoid Robotics.

This work aligns with the vision of **Panaversity**:

* 🌐 [https://panaversity.org](https://panaversity.org)
* 📖 [https://ai-native.panaversity.org](https://ai-native.panaversity.org)

---

## ✅ Hackathon Requirements — Fully Implemented

### 1️⃣ AI / Spec‑Driven Book Creation (100% Complete)

* 📚 AI‑Native textbook authored using **Claude Code**
* 🧩 Structured and governed using **Spec‑Kit Plus**
* 🧱 Built with **Docusaurus** for scalable documentation
* 🚀 Deployed successfully on **Vercel/ HuggingFace**

✔ The book content strictly follows spec‑driven development principles
✔ Chapters, sections, and learning flow are AI‑assisted and spec‑validated

---

### 2️⃣ Integrated RAG Chatbot (100% Complete)

An **embedded Retrieval‑Augmented Generation (RAG) chatbot** is fully implemented inside the book.

#### 🔧 Technology Stack

* **OpenAI Agents / ChatKit SDK**
* **FastAPI** backend
* **Cohere**
* **Qdrant Cloud (Free Tier)** for vector search

#### 🧠 Capabilities

* ✅ Answers questions using **only the book content**
* ✅ Can answer questions based on **user‑selected text only**
* ✅ Context‑aware, chapter‑aware responses
* ✅ Real‑time interaction inside the textbook UI

---

### 3️⃣ Authentication & Personalization (Bonus Points Implemented)

* 🔐 **Signup & Signin implemented using Better‑Auth**
* 🧑‍💻 During signup, users are asked about:

  * Software background
  * Hardware / robotics experience

#### 🎯 Personalization

Based on user background:

* Content difficulty is adapted
* Explanations are personalized
* Examples are tailored to user skill level

---

### 4️⃣ Reusable Intelligence (Bonus Points Implemented)

* 🤖 **Claude Code Sub‑Agents** used for:

  * Chapter generation
  * Concept explanations
  * Quiz and glossary creation

* 🧠 **Agent Skills** reused across chapters

* ♻️ Modular, scalable AI workflows

---

## 🧱 Project Architecture

```
my-ai-robotics-book/
│
├── backend/                 # FastAPI backend (RAG, Auth, Agents)
├── my-ai-robotics-book/     # Docusaurus frontend (Textbook UI)
├── specs/                   # Spec‑Kit Plus specifications
├── .claude/                 # Claude Code agents & configs
├── CLAUDE.md                # AI instructions & system rules
├── package.json             # Frontend dependencies
├── README.md                # Project documentation
```

---

## 🚀 Local Development

### Prerequisites

* Node.js (v18+ recommended)
* Python 3.10+
* Git

### Frontend (Book)

```bash
npm install
npm run start
```

### Backend (RAG + Auth)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🌐 Deployment

* 📘 Book deployed on **Vercel**
* ⚙️ Backend deployed on **Huggingface**
* 🧠 Vector DB hosted on **Qdrant Cloud**
* 🗄️ Database hosted on **Cohere**

---

## 🎓 Educational Impact

This project is designed to:

* Teach **Physical AI & Humanoid Robotics** effectively
* Enable **AI‑assisted learning**
* Support **self‑paced, personalized education**
* Act as a foundation for future **AI‑Native textbooks**

---

## 👩‍💻 Author

**Muniza Nabeel**
AI‑Native Developer | Hackathon Participant

---

## 🏅 Hackathon Status

✅ All base requirements completed (100/100)
✅ Reusable Intelligence implemented (+50)
✅ Authentication & Personalization implemented (+50)

**Project is production‑ready and fully functional.**

---

## 📄 License

This project is released under the **MIT License**.

---

✨ *Built with vision, discipline, and AI‑Native principles — aligned with the future of education.*
