# 🤖 Nexus AI Agent

> A production-grade custom LLM Agent built with **FastAPI + LangChain + React**
> Features real-time streaming, multi-tool calling, and conversation memory.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-0.3-purple?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-black?style=flat-square)

---

## 🎥 Demo

> Chat with an AI agent that can search the web, run Python code, read files, query databases, and perform calculations — all in real time.

---

## ✨ Features

- 🔄 **Real-time Streaming** — Token-by-token responses via Server-Sent Events (SSE)
- 🛠️ **5 Built-in Tools** — Web search, Python executor, file reader, calculator, database query
- 🧠 **Conversation Memory** — Remembers last 10 turns of context
- ⚡ **FastAPI Backend** — Async, production-ready REST API
- ⚛️ **React Frontend** — Clean dark UI with live tool-call visualization
- 🔌 **Easily Extensible** — Add new tools in minutes with `@tool` decorator

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI GPT-4o |
| Agent Framework | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | React 18 + Vite |
| Search Tool | DuckDuckGo |
| Streaming | Server-Sent Events |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/nexus-agent.git
cd nexus-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Add your OpenAI API key in `backend/.env`:
```
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4o
```

Start the backend:
```bash
uvicorn main:app --reload
# Running on http://localhost:8000
```

### 3. Frontend Setup
```bash
# Open a new terminal
cd frontend
npm install
npm run dev
# Running on http://localhost:3000
```

### 4. Open in browser
```
http://localhost:3000
```

---

## 🧰 Available Tools

| Tool | What it does |
|------|-------------|
| `web_search` | Search the internet in real-time |
| `code_executor` | Write and run Python code |
| `file_reader` | Read PDF, CSV, JSON, TXT files |
| `calculator` | Precise math and formulas |
| `database_query` | Query structured data |

### Adding a Custom Tool (super easy)

```python
# backend/tools.py
from langchain.tools import tool

@tool
def my_tool(input: str) -> str:
    """Describe what this tool does."""
    return do_something(input)
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get full response |
| POST | `/chat/stream` | Send a message, get SSE stream |
| GET | `/tools` | List available tools |
| DELETE | `/conversation/{id}` | Clear conversation memory |
| GET | `/health` | Health check |

---

## 📁 Project Structure

```
nexus-agent/
├── backend/
│   ├── main.py        ← FastAPI app + API routes
│   ├── agent.py       ← LangChain agent + memory
│   ├── tools.py       ← All 5 tools defined here
│   ├── requirements.txt
│   └── .env           ← Your API key (never commit this!)
└── frontend/
    └── src/
        ├── App.jsx          ← Main UI
        ├── components/
        │   ├── Sidebar.jsx  ← Tools panel
        │   └── Message.jsx  ← Chat messages
        ├── hooks/
        │   └── useAgent.js  ← Streaming state
        └── utils/
            └── api.js       ← API calls
```

---

## 💼 Use Cases

This agent can be customized for any client need:

- **Customer Support Bot** — Connect to CRM or ticketing system
- **Data Analysis Assistant** — Query databases, generate reports
- **Document Intelligence** — Process PDFs, contracts, invoices
- **Research Assistant** — Automated web research + summarization
- **Internal Knowledge Base** — RAG over company documents
- **Code Review Bot** — Analyze and improve repositories

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | required | Your OpenAI API key |
| `MODEL_NAME` | `gpt-4o` | LLM model to use |

---

## 👨‍💻 About the Developer

Full Stack AI Engineer specializing in:
- **LLM Applications** — LangChain, LlamaIndex, RAG pipelines
- **Computer Vision** — YOLO, OpenCV, image classification
- **Backend** — FastAPI, Django, REST APIs
- **Frontend** — React, Next.js
- **MLOps** — Model deployment, Docker

📫 Available for freelance projects on **Upwork**

---

## 📄 License

MIT License — free to use for commercial projects.

---

⭐ **Star this repo if it helped you!**
