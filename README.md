# 🤖 Local LLM Chatbot
 
### Privacy-First AI Assistant Running Entirely On Your Laptop
 
[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-0.30.6-white?logo=ollama)](https://ollama.com)
[![Llama](https://img.shields.io/badge/Llama_3.1-8B-purple)](https://ollama.com/library/llama3.1)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
 
> A fully local, privacy-first AI chatbot built with Flask and Ollama —
> no API keys, no internet required, no data leaving your laptop.
> Features a modern chat UI with dark/light mode, real-time weather,
> web search, and conversation memory.
 
---
 
## 💡 Why This Project
 
Most AI chatbots send your data to external servers — OpenAI, Google, Anthropic. For individuals handling sensitive information, and especially for enterprises in banking, healthcare, or government, this is a non-starter. Data privacy regulations, compliance requirements, and confidentiality concerns make cloud-based AI inaccessible for many real-world use cases.
 
This project explores a different approach: running a capable open-weight large language model entirely on local hardware. No data leaves the machine. No API costs. No rate limits. The result is a functional, modern AI assistant that demonstrates how privacy-first AI can work in practice — a skill increasingly valued in enterprise data science roles.
 
---

## 📌 Project Overview
 
This project builds an end-to-end local AI chatbot with a browser-based UI, backed by Llama 3.1 8B running through Ollama. It demonstrates how open-weight models can be deployed locally with real-time data augmentation, conversation memory, and a polished interface — without touching any paid service.
 
**Core Features:**
- 🧠 Llama 3.1 8B running locally via Ollama (Q4 quantisation, ~5GB RAM)
- 💬 Full conversation memory — AI remembers context across the session
- 🌤️ Live weather via Open-Meteo API (free, no key needed)
- 🔍 Web search via DuckDuckGo Instant Answer API (free, no key)
- 🕐 Real-time date and time awareness
- 🌙 Dark / Light mode toggle with preference persistence
- ⚡ Typing indicator, auto-resize input, Enter to send

---

## 📸 Screenshots
 
| **Dark Mode** | **Light Mode** |
|---|---|
| ![Dark Mode](Figures/Local_LLM_Chatbot(1).png) | ![Light Mode](Figures/Local_LLM_Chatbot(2).png) |
 
> Dark mode (default) and light mode — toggle available in the sidebar.
 
---

## 🛠️ Tech Stack
 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-ffffff?style=for-the-badge)](https://ollama.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
 
| Category | Tool | Purpose |
|---|---|---|
| **Model Runner** | Ollama 0.30.6 | Downloads and runs Llama 3.1 locally |
| **AI Model** | Llama 3.1 8B (Q4) | Open-weight LLM by Meta, runs in ~5GB RAM |
| **Backend** | Flask 3.1 | Local web server and API routing |
| **AI Client** | Ollama Python SDK 0.6.2 | Python interface to Ollama |
| **Real-time Data** | Open-Meteo, DuckDuckGo | Free APIs, no signup required |
| **Frontend** | HTML, CSS, Vanilla JS | Chat UI served by Flask |
 
---

## 📁 Project Structure
 
```
Local LLM Chatbot/
│
├── app.py                  ← Flask server and API routes
├── ollama_client.py        ← Ollama connection, chat history, real-time features
├── requirements.txt        ← Python dependencies
│
├── templates/
│   └── index.html          ← Chat UI rendered in browser
│
└── static/
    ├── style.css           ← Dark/light theme, chat bubble styling
    └── script.js           ← Message handling, theme toggle, typing indicator
```
 
---
 
## 🔄 How It Works
 
```
You type a message in browser
        ↓
script.js detects intent (weather / search / datetime / chat)
        ↓
Sends POST request to Flask (app.py) at /chat
        ↓
app.py calls ollama_client.py
        ↓
ollama_client.py fetches real-time data if needed
(Open-Meteo for weather, DuckDuckGo for search, datetime for time)
        ↓
Real-time data + your message sent to Llama 3.1 via Ollama
        ↓
Llama processes entirely on your laptop — zero internet
        ↓
Response returns to browser as a chat bubble
```
 
---

## 💬 What You Can Ask
 
| Type | Example Prompts |
|---|---|
| **General knowledge** | "Explain machine learning in simple terms" |
| **Coding help** | "Write a Python function to clean a dataframe" |
| **Weather** | "What's the weather in Mumbai?" |
| **Date & Time** | "What time is it?" / "What day is today?" |
| **Web search** | "Search for black holes" / "Who is Elon Musk?" |
| **Writing** | "Write a professional email declining a meeting" |
| **Data Science** | "Explain the difference between precision and recall" |
 
---
 
## 🔑 Key Concepts Demonstrated
 
**Model Quantisation** — Llama 3.1 8B runs at Q4 quantisation, compressing the model from ~16GB to ~5GB with minimal quality loss. Understanding this size vs quality tradeoff is essential for deploying LLMs in resource-constrained environments.
 
**Local Inference** — The model runs entirely on CPU/GPU on your laptop. No data is transmitted externally at any point — demonstrating how privacy-first AI works without cloud dependency.
 
**Retrieval Augmentation** — Real-time data (weather, search results, datetime) is fetched and injected into the prompt before sending to the model, giving the LLM access to current information it wasn't trained on.
 
**Conversation Memory** — The full conversation history is sent with every request, giving the model context across multiple turns — the same mechanism used by production chatbots.
 
---
 
## ⚠️ Limitations
 
- **No image support** — Llama 3.1 8B is text-only; multimodal models require more RAM
- **DuckDuckGo search** — Instant Answer API returns best-effort results; complex queries may not resolve
- **RAM dependent** — Q4 quantisation requires ~5-6GB free RAM; performance degrades if RAM is heavily used
- **Development server** — Flask's built-in server is for local use only; a WSGI server (Gunicorn) is needed for production deployment
---
 
## 🚀 Future Improvements
 
- **Add Mistral 7B** — pull `ollama pull mistral` and enable model switching to compare outputs
- **PDF chat** — upload a document and ask questions about it using LangChain's document loaders
- **Streaming responses** — stream tokens as they generate for a more responsive feel
- **Voice input** — integrate Web Speech API for voice-to-text queries
- **Chat export** — save conversation history as PDF or text file
---
 
## 👤 Author
 
**Ishan Abrol**
 
*Building privacy-first AI tools as part of an end-to-end data science portfolio.*
