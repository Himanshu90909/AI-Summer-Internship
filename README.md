# MirAI School of Technology - Virtual Summer Internship 2026
# Capstone Mini-Project: The Multi-Modal Visual Novel

A "Choose Your Own Adventure" Visual Novel Engine built with Streamlit that orchestrates:
- **Gemini AI** for structured JSON story generation
- **Pollinations AI** for dynamic scene illustrations
- **gTTS** for text-to-speech narration
- **Dynamic UI rendering** with AI-generated choice buttons

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey).

You can either:
1. Paste the key in the sidebar when the app loads
2. Set it as an environment variable: `export GOOGLE_API_KEY=your_key`

## How It Works

1. **Phase 1 - Configuration**: Select genre and art style in the sidebar. The Gemini client is cached with `@st.cache_resource`.
2. **Phase 2 - Structured JSON**: Gemini returns responses as JSON with `story_text`, `image_prompt`, and `options` keys, parsed with Python's `json` library.
3. **Phase 3 - Dynamic UI**: A for-loop generates `st.button()` components from the AI's options list.
4. **Phase 4 - Multi-Media**: Pollinations generates scene images, gTTS narrates the story text via `st.audio()`.
5. **Phase 5 - Graceful Failures**: All API calls wrapped in `try/except` with `st.toast()` notifications.

## Technologies
- Python · Streamlit · Google Gemini API · Pollinations AI · gTTS · JSON Parsing · Session State Management
