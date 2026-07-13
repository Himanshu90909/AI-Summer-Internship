import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Multiverse Chatbot", page_icon="🌌")
st.title("🌌 Multiverse Chatbot")


with st.sidebar:
    st.header("⚙️ Settings")
    personality = st.selectbox(
        "Choose a personality:",
        ["Friendly Guide", "Sarcastic Robot", "Wise Wizard", "Pirate Captain"],
    )
    st.caption("Changing this will NOT wipe your chat history 👍")

PERSONALITY_PROMPTS = {
    "Friendly Guide": "You are a warm, encouraging, and friendly assistant.",
    "Sarcastic Robot": "You are a sarcastic, witty robot who loves dry humor.",
    "Wise Wizard": "You are an ancient, wise wizard who speaks in riddles and metaphors.",
    "Pirate Captain": "You are a swashbuckling pirate captain who talks like a pirate.",
}

# Put your API key in .streamlit/secrets.toml as:
# GEMINI_API_KEY = "your-api-key-here"
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("Say something..."):

    # Save + display the user's message
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Build a short conversation-aware prompt using the personality + history
    system_instruction = PERSONALITY_PROMPTS[personality]
    history_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages
    )
    full_prompt = f"{system_instruction}\n\nConversation so far:\n{history_text}\n\nASSISTANT:"

    # Get the AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(full_prompt)
            st.markdown(response.text)

    # Save the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response.text})
