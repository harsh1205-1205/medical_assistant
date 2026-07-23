import os
import streamlit as st
from groq import Groq

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

if not API_KEY:
    st.error("Missing GROQ_API_KEY environment variable. Please set it before running the app.")
    st.stop()

SYSTEM_PROMPT = """
You are a medical assistant chatbot.
Provide general health information only. Do not diagnose or claim certainty.
Encourage the user to seek medical care from a licensed clinician for emergencies or serious symptoms.
If symptoms are severe, urgent, or life-threatening, tell them to contact emergency services or seek immediate medical attention.
Keep responses concise, clear, and helpful.
"""

st.set_page_config(page_title="Medical Assistant", page_icon="🩺", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #d9ecff 0%, #8bbcff 100%);
            color: #0a2140 !important;
        }

        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid #6bb2ff !important;
            border-radius: 12px !important;
            padding: 0.7rem 0.9rem !important;
            color: #0a2140 !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span {
            color: #0a2140 !important;
        }

        [data-testid="stChatInput"] {
            background: #ffffff !important;
            color: #0a2140 !important;
            border: 1px solid #5aa7ff !important;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            color: #0a2140 !important;
            background: #ffffff !important;
        }

        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder {
            color: #557299 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🩺 Medical Assistant Chatbot")
st.caption("Ask general medical questions and get a response from Groq's LLM model.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your medical question here...")

if user_input:
    client = Groq(api_key=API_KEY)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.2,
                max_tokens=300,
                stream=True,
            )

            answer = ""
            response_placeholder = st.empty()
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    answer += delta
                    response_placeholder.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
