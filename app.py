"""
MirAI School of Technology - Virtual Summer Internship 2026
Capstone Mini-Project: The Multi-Modal Visual Novel
The "AI Builder" Track

A "Choose Your Own Adventure" Visual Novel Engine built with Streamlit.
Orchestrates: Gemini (structured JSON), Pollinations (visuals), gTTS (audio narration).
"""

import json
import os
import io
import time
import urllib.request
import urllib.error
from PIL import Image

import streamlit as st
import google.generativeai as genai
from gtts import gTTS


# ============================================================
# PHASE 1: The Director's Cut (UI & Configuration)
# ============================================================

@st.cache_resource
def get_gemini_client(api_key):
    """
    Securely cache the Gemini client using @st.cache_resource.
    This ensures we don't re-initialize the client on every Streamlit rerun.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    return model


# The system prompt instructs Gemini to ALWAYS return structured JSON.
# This is the backbone of Phase 2 — the Structured JSON Engine.
SYSTEM_PROMPT = """You are the narrator of a "Choose Your Own Adventure" visual novel.

CRITICAL: You must ALWAYS respond with a valid JSON object and NOTHING else.
No markdown, no code fences, no commentary — just raw JSON.

The JSON object must contain exactly these three keys:

1. "story_text": A vivid, immersive narrative paragraph (2-4 sentences) describing
   what happens next in the story based on the user's choice. Be descriptive and
   atmospheric — set the scene for the reader.

2. "image_prompt": A heavily engineered prompt for an AI image generator. This should
   be a detailed, visual description of the current scene that would produce a stunning
   illustration. Include art style, lighting, mood, composition details, and specific
   visual elements mentioned in the story text.

3. "options": A JSON array of 2 to 3 strings, each representing a distinct choice the
   player can make next. Each option should be a short, action-oriented phrase (e.g.,
   "Open the mysterious door", "Search the room for clues", "Run away").

Here is an example of the exact format you must follow:

{
  "story_text": "You step into the dimly lit chamber. Ancient carvings line the walls, glowing faintly with an otherworldly blue light. In the center sits a pedestal with a shimmering orb.",
  "image_prompt": "Digital painting of an ancient stone chamber with glowing blue wall carvings, a pedestal with a luminous orb in the center, dramatic lighting, cinematic composition, fantasy art style, highly detailed, atmospheric mist",
  "options": ["Touch the glowing orb", "Examine the wall carvings", "Leave the chamber"]
}

RULES:
- Always return valid, parseable JSON.
- Keep the story moving forward — never repeat the same scene.
- Match the genre and art style specified by the user.
- Make each choice meaningful and distinct.
- If the story reaches a natural ending, set "options" to ["Start a new adventure"].
"""


def init_session_state():
    """Initialize st.session_state to store chat history and Gemini chat object."""
    if "chat" not in st.session_state:
        st.session_state.chat = None
    if "history" not in st.session_state:
        st.session_state.history = []  # list of {role, text, image, audio, options}
    if "story_started" not in st.session_state:
        st.session_state.story_started = False
    if "genre" not in st.session_state:
        st.session_state.genre = "Fantasy"
    if "art_style" not in st.session_state:
        st.session_state.art_style = "Digital Painting"


# ============================================================
# PHASE 2: The Structured JSON Engine
# ============================================================

def get_story_response(user_input, genre, art_style):
    """
    Send the user's choice to Gemini and parse the JSON response.

    Uses Python's built-in json library to parse the AI's string response
    into a usable Python dictionary with story_text, image_prompt, and options.
    """
    # Build the full prompt with genre and art style context
    context_prompt = f"""
    Genre: {genre}
    Art Style: {art_style}

    The user's action: {user_input}

    Respond with the JSON object now. Remember: ONLY JSON, no other text.
    """

    # Get response from Gemini
    response = st.session_state.chat.send_message(context_prompt)
    raw_text = response.text.strip()

    # Clean up: Gemini sometimes wraps JSON in markdown code fences
    if raw_text.startswith("```"):
        # Remove ```json or ``` at the start and ``` at the end
        raw_text = raw_text.split("\n", 1)[1] if "\n" in raw_text else raw_text
        raw_text = raw_text.replace("```", "").strip()
        # If it started with ```json, remove that prefix
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()

    # Parse the JSON string into a Python dictionary
    try:
        story_data = json.loads(raw_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the text
        try:
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            if start != -1 and end > start:
                story_data = json.loads(raw_text[start:end])
            else:
                raise
        except (json.JSONDecodeError, ValueError):
            # Fallback: create a minimal valid response
            st.toast("⚠️ AI response format issue — generating fallback story...")
            story_data = {
                "story_text": raw_text[:500] if raw_text else "The story continues, but the path ahead is unclear...",
                "image_prompt": f"{art_style} style scene, {genre} genre, atmospheric, dramatic lighting",
                "options": ["Continue the adventure", "Try something different"]
            }

    # Validate required keys exist
    if "story_text" not in story_data:
        story_data["story_text"] = "The adventure continues..."
    if "image_prompt" not in story_data:
        story_data["image_prompt"] = f"{art_style} style, {genre} scene, atmospheric"
    if "options" not in story_data or not isinstance(story_data["options"], list):
        story_data["options"] = ["Continue", "Explore elsewhere"]

    return story_data


# ============================================================
# PHASE 4: Visual Asset Generation (Pollinations API)
# ============================================================

def generate_image(image_prompt, art_style):
    """
    Send the parsed image_prompt to the Pollinations API.
    Downloads and returns a PIL Image object.

    Wrapped in try/except for graceful failure (Phase 5).
    """
    # Engineer the final prompt with art style
    full_prompt = f"{image_prompt}, {art_style} style, highly detailed, cinematic"

    # Pollinations API endpoint
    seed = int(time.time()) % 1000000
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=512&seed={seed}&nologo=true"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(req, timeout=30)
    img_data = response.read()

    img = Image.open(io.BytesIO(img_data))
    return img


# ============================================================
# PHASE 4: Audio Integration (gTTS - Text-to-Speech)
# ============================================================

def generate_narration_audio(story_text):
    """
    Use gTTS (Google Text-to-Speech) to convert the AI's story_text
    into an audio file. Returns a BytesIO buffer for st.audio() playback.
    """
    tts = gTTS(text=story_text, lang="en", slow=False)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    st.set_page_config(
        page_title="Visual Novel Engine",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for a polished visual novel aesthetic
    st.markdown("""
    <style>
    .stApp { background: #0a0a12; }
    .story-text {
        font-size: 18px;
        line-height: 1.8;
        color: #e0e0e8;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        border-left: 3px solid #7c5cff;
        margin: 10px 0;
    }
    .scene-title {
        font-size: 24px;
        font-weight: 700;
        color: #7c5cff;
        margin-bottom: 10px;
    }
    .choice-label {
        font-size: 14px;
        color: #9b9ba5;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    div.stButton > button {
        width: 100%;
        text-align: left;
        padding: 12px 16px;
        border: 1px solid #2a2a3a;
        border-radius: 10px;
        background: rgba(124, 92, 255, 0.1);
        color: #e0e0e8;
        font-size: 15px;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: rgba(124, 92, 255, 0.25);
        border-color: #7c5cff;
        transform: translateX(4px);
    }
    </style>
    """, unsafe_allow_html=True)

    init_session_state()

    # ============================================================
    # SIDEBAR: Story Settings (Phase 1)
    # ============================================================
    with st.sidebar:
        st.markdown("## 🎭 Story Settings")

        genre = st.selectbox(
            "📖 Story Genre",
            ["Fantasy", "Sci-Fi", "Horror", "Mystery", "Adventure",
             "Cyberpunk", "Post-Apocalyptic", "Steampunk", "Noir Detective"],
            index=["Fantasy", "Sci-Fi", "Horror", "Mystery", "Adventure",
                   "Cyberpunk", "Post-Apocalyptic", "Steampunk", "Noir Detective"].index(st.session_state.genre)
        )

        art_style = st.selectbox(
            "🎨 Art Style",
            ["Digital Painting", "Anime", "Watercolor", "Oil Painting",
             "Pixel Art", "Comic Book", "Photorealistic", "Concept Art",
             "Studio Ghibli Style", "Dark Fantasy"],
            index=["Digital Painting", "Anime", "Watercolor", "Oil Painting",
                   "Pixel Art", "Comic Book", "Photorealistic", "Concept Art",
                   "Studio Ghibli Style", "Dark Fantasy"].index(st.session_state.art_style)
        )

        st.session_state.genre = genre
        st.session_state.art_style = art_style

        st.markdown("---")

        # Gemini API key input (falls back to environment variable)
        env_key = os.environ.get("GOOGLE_API_KEY", "")
        api_key = st.text_input(
            "🔑 Gemini API Key",
            value=env_key,
            type="password",
            help="Get your free key at https://aistudio.google.com/apikey. "
                 "Or set the GOOGLE_API_KEY environment variable."
        )

        st.markdown("---")

        if st.button("🔄 Start New Adventure", use_container_width=True):
            st.session_state.history = []
            st.session_state.story_started = False
            st.session_state.chat = None
            st.rerun()

        st.markdown("---")
        st.caption("Built for MirAI School of Technology")
        st.caption("Virtual Summer Internship 2026")

    # ============================================================
    # MAIN CONTENT AREA
    # ============================================================

    st.markdown("# 🎭 The Multi-Modal Visual Novel")
    st.markdown(f"*Genre: {genre} · Art Style: {art_style}*")
    st.markdown("---")

    # Check for API key
    if not api_key:
        st.warning("👈 Enter your Gemini API key in the sidebar to begin your adventure.")
        st.info("Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey)\n"
                 "Or set the environment variable: `export GOOGLE_API_KEY=your_key`")
        return

    # Initialize Gemini client (cached via @st.cache_resource)
    try:
        model = get_gemini_client(api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return

    # Initialize or reset chat object when genre/art_style changes
    if st.session_state.chat is None:
        st.session_state.chat = model.start_chat(history=[])

    # Start the story if not yet begun
    if not st.session_state.story_started:
        st.session_state.story_started = True
        opening_prompt = f"Start a new {genre} story with {art_style} art style. Set the opening scene and give the player their first choices."
        process_story_turn(opening_prompt, genre, art_style, is_opening=True)

    # ============================================================
    # RENDER STORY HISTORY (using st.session_state so nothing disappears)
    # ============================================================
    for i, entry in enumerate(st.session_state.history):
        render_story_entry(entry, i)

    # ============================================================
    # PHASE 3: Dynamic UI Generation
    # ============================================================
    # The latest entry's options become dynamically generated buttons.
    if st.session_state.history:
        latest = st.session_state.history[-1]
        options = latest.get("options", [])

        if options:
            st.markdown('<p class="choice-label">🎮 What do you do?</p>', unsafe_allow_html=True)

            # Write a for loop that iterates over the options list
            # and dynamically generates an st.button() for each choice.
            for idx, option in enumerate(options):
                if st.button(f"➤ {option}", key=f"choice_{len(st.session_state.history)}_{idx}"):
                    # The clicked button's text is sent to Gemini as the user's next move
                    process_story_turn(option, genre, art_style)
                    st.rerun()


def process_story_turn(user_input, genre, art_style, is_opening=False):
    """
    Process a single story turn:
    1. Call Gemini for structured JSON (Phase 2)
    2. Generate image via Pollinations (Phase 4)
    3. Generate TTS audio (Phase 4)
    4. Store everything in session_state
    All wrapped in try/except for graceful failures (Phase 5).
    """
    with st.spinner("📖 Weaving the next chapter of your story..."):

        # --- PHASE 2: Get structured JSON from Gemini ---
        try:
            story_data = get_story_response(user_input, genre, art_style)
        except Exception as e:
            st.toast(f"⚠️ Story generation issue: {str(e)[:100]}")
            story_data = {
                "story_text": "The path ahead is shrouded in mist. You must choose your next step carefully...",
                "image_prompt": f"{art_style} style, {genre} scene, foggy, mysterious, atmospheric",
                "options": ["Press forward", "Turn back"]
            }

        story_text = story_data["story_text"]
        image_prompt = story_data["image_prompt"]
        options = story_data["options"]

        # --- PHASE 4: Generate image via Pollinations ---
        image = None
        try:
            image = generate_image(image_prompt, art_style)
        except urllib.error.URLError:
            st.toast("🖼️ Image server is busy, skipping visual...")
        except Exception:
            st.toast("🖼️ Image server is busy, skipping visual...")
        # If image fails, story continues without crashing (Phase 5)

        # --- PHASE 4: Generate TTS audio ---
        audio_buffer = None
        try:
            audio_buffer = generate_narration_audio(story_text)
        except Exception:
            st.toast("🔊 Audio narration unavailable, continuing with text only...")
        # If audio fails, story continues without crashing (Phase 5)

        # --- Store in session_state so nothing disappears on rerun ---
        entry = {
            "story_text": story_text,
            "image": image,
            "audio": audio_buffer,
            "options": options,
            "is_opening": is_opening
        }
        st.session_state.history.append(entry)


def render_story_entry(entry, index):
    """
    Render a single story entry: image, text, and audio.
    Uses st.session_state data so content persists across reruns.
    """
    if entry.get("is_opening"):
        st.markdown('<p class="scene-title">🌟 The Adventure Begins</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="scene-title">📖 Scene {index + 1}</p>', unsafe_allow_html=True)

    # Render image (if available)
    if entry.get("image"):
        st.image(entry["image"], use_container_width=True)

    # Render story text
    st.markdown(f'<div class="story-text">{entry["story_text"]}</div>', unsafe_allow_html=True)

    # Render audio narration (if available)
    if entry.get("audio"):
        st.audio(entry["audio"], format="audio/mp3")

    st.markdown("---")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
