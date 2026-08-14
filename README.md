# MirAI School of Technology — Virtual Summer Internship 2026

This repository contains all tasks and the capstone project for the **MirAI School of Technology Virtual Summer Internship 2026** (AI Builder Track).

---

## Capstone Project: The Multi-Modal Visual Novel Engine

A "Choose Your Own Adventure" Visual Novel Engine built with Streamlit that orchestrates:
- **Gemini AI** for structured JSON story generation
- **Pollinations AI** for dynamic scene illustrations
- **gTTS** for text-to-speech narration
- **Dynamic UI rendering** with AI-generated choice buttons

### Setup

```bash
pip install -r requirements.txt
```

### Running

```bash
streamlit run app.py
```

Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey).

You can either:
1. Paste the key in the sidebar when the app loads
2. Set it as an environment variable: `export GOOGLE_API_KEY=your_key`

### How It Works

1. **Phase 1 — Configuration**: Select genre and art style in the sidebar. The Gemini client is cached with `@st.cache_resource`.
2. **Phase 2 — Structured JSON**: Gemini returns responses as JSON with `story_text`, `image_prompt`, and `options` keys, parsed with Python's `json` library.
3. **Phase 3 — Dynamic UI**: A `for`-loop generates `st.button()` components from the AI's options list.
4. **Phase 4 — Multi-Media**: Pollinations generates scene images, gTTS narrates the story text via `st.audio()`.
5. **Phase 5 — Graceful Failures**: All API calls wrapped in `try/except` with `st.toast()` notifications.

---

## Task Submissions

### Task 1 — Echo Chamber 9000 (`Task-1.html`)
A standalone HTML page with a retro-terminal aesthetic. Features AI echo simulation, animated meters, and real-time log output. Pure HTML/CSS/JS — no dependencies.

### Task 2 — Multiverse AI (`Task-2.html`)
A ChatGPT-style conversational UI clone with sidebar navigation, chat history, composer, and model picker. Full state management with vanilla JS. Pure HTML/CSS/JS — no dependencies.

### Task 3 — Multiverse Chatbot (`Task-3.py`)
A Streamlit chatbot with swappable AI personalities (Friendly Guide, Sarcastic Robot, Wise Wizard, Pirate Captain). Uses Google Gemini for responses with conversation history via `st.session_state`.

**Setup:** Create `.streamlit/secrets.toml` with:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

**Run:** `streamlit run Task-3.py`

### Task 4 — Task Management App (`Task-4-App.jsx`)
A React task management application with categories, priority levels, due dates, status tracking, dark/light mode, and local storage persistence. Full component architecture using React Context API.

**Files:** `Task-4.md` (documentation), `Task-4-App.jsx` (main component), `TaskApp.css` (styles)

---

## Bonus Project: AI Image Studio

A React + TailwindCSS app for generating AI images using the Pollinations AI API. Features multiple art styles, custom dimensions, and a magic enhance toggle.

**Setup:**
```bash
npm install
npm run dev
```

**Tech:** React 18 · Vite · TailwindCSS · Pollinations AI

---

## Technologies Used
- Python · Streamlit · Google Gemini API · Pollinations AI · gTTS · JSON Parsing · Session State
- React 18 · Vite · TailwindCSS · JavaScript (ES6+)
- HTML5 · CSS3 · Vanilla JS

## License
MIT License — Copyright (c) 2026 Himanshu Suthar
