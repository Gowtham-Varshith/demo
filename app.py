import streamlit as st
from agent import ask_ai_stream, fake_ai_response

# -------- CONFIG --------
st.set_page_config(page_title="AI Assistant", layout="wide")

# -------- PREMIUM CSS + BUBBLES --------
st.markdown("""
<style>

/* Background gradient */
body {
    background: linear-gradient(135deg, #020617, #0f172a);
}

/* Floating bubbles */
.bubble {
    position: fixed;
    bottom: -100px;
    width: 40px;
    height: 40px;
    background: rgba(99,102,241,0.3);
    border-radius: 50%;
    animation: rise 15s infinite ease-in;
}

@keyframes rise {
    0% { transform: translateY(0); opacity:0; }
    50% { opacity:0.6; }
    100% { transform: translateY(-100vh); opacity:0; }
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 12px;
    margin: 10px 0;
}

[data-testid="stChatMessage"][data-author="user"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
}

[data-testid="stChatMessage"][data-author="assistant"] {
    background: rgba(30,41,59,0.7);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Title */
h1 {
    text-align:center;
    font-size:2.5rem;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

</style>

<div class="bubble" style="left:10%"></div>
<div class="bubble" style="left:30%"></div>
<div class="bubble" style="left:50%"></div>
<div class="bubble" style="left:70%"></div>
<div class="bubble" style="left:90%"></div>

""", unsafe_allow_html=True)

# -------- TITLE --------
st.markdown("<h1>🤖 AI Assistant (Final Boss UI)</h1>", unsafe_allow_html=True)

# -------- MODE --------
mode = st.sidebar.selectbox("Mode", ["Local AI (Ollama)", "Demo (Cloud)"])

# -------- MEMORY --------
if "chat" not in st.session_state:
    st.session_state.chat = []

# -------- INPUT --------
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.chat.append(("You", user_input))
    st.chat_message("user").write(user_input)

    msg_box = st.chat_message("assistant").empty()

    full_reply = ""

    if mode == "Local AI (Ollama)":
        for chunk in ask_ai_stream(f"Answer briefly:\n{user_input}"):
            full_reply = chunk
            msg_box.write(full_reply)

    else:
        # cloud demo fallback
        full_reply = fake_ai_response(user_input)
        msg_box.write(full_reply)

    st.session_state.chat.append(("AI", full_reply))

# -------- HISTORY --------
for role, msg in st.session_state.chat[:-1]:
    if role == "You":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)