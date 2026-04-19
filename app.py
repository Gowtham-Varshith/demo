import streamlit as st
import requests
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Demo-Gowtham-Ai agent", page_icon="🤖")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: right;
    color: white;
    font-size: 15px;
}

.bot-msg {
    background: #1e293b;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    color: #e2e8f0;
    font-size: 15px;
}

/* Chat input spacing */
.stChatInput {
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🤖 Demo-Gowtham-Ai agent")

# ---------------- STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- PDF UPLOAD ----------------
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

if uploaded_file:
    try:
        requests.post(
            "http://127.0.0.1:8000/upload",
            files={"file": uploaded_file}
        )
        st.success("PDF uploaded successfully ✅")
    except:
        st.error("Backend not running ❌")

# ---------------- DISPLAY CHAT ----------------
for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.chat.append(("user", user_input))

    # 🔥 SHOW LOADING SPINNER
    with st.spinner("🤖 Thinking..."):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": user_input}
            )
            reply = res.json()["reply"]
        except:
            reply = "⚠️ Backend error"

    # 🔥 TYPING ANIMATION EFFECT
    placeholder = st.empty()
    typed_text = ""

    for char in reply:
        typed_text += char
        placeholder.markdown(
            f'<div class="bot-msg">{typed_text}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    # Save final message
    st.session_state.chat.append(("bot", reply))