import requests
from PyPDF2 import PdfReader
from rapidfuzz import fuzz

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# ---------------- MEMORY ----------------
chat_history = []

# ---------------- PDF STORE ----------------
pdf_store = {
    "text": ""
}

# ---------------- LLM (FAST VERSION) ----------------
def ask_llama(prompt: str) -> str:
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:instruct",  # 🔥 faster model
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 150,      # 🔥 limit output
                    "temperature": 0.7
                }
            }
        )
        return res.json().get("response", "")
    except:
        return "⚠️ Ollama not running or error occurred"


# ---------------- PDF LOADER ----------------
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # 🔥 reduced size for speed
    pdf_store["text"] = text[:1500]


# ---------------- INTENT DETECTION ----------------
def is_pdf_request(text: str) -> bool:
    return (
        fuzz.partial_ratio(text, "summarize pdf") > 70 or
        fuzz.partial_ratio(text, "explain pdf") > 70 or
        fuzz.partial_ratio(text, "what is in the pdf") > 70 or
        fuzz.partial_ratio(text, "tell me about the pdf") > 70
    )


# ---------------- AGENT ----------------
def ai_agent(user_input: str) -> str:
    global chat_history

    chat_history.append(user_input)
    text = user_input.lower()

    # ---------------- PDF HANDLING ----------------
    if is_pdf_request(text):
        if pdf_store["text"] == "":
            return "📄 Please upload a PDF first."

        prompt = f"""
        Summarize and explain this document simply:

        {pdf_store["text"]}
        """

        return ask_llama(prompt)

    # ---------------- CALCULATOR ----------------
    if "calculate" in text:
        try:
            expression = text.replace("calculate", "")
            return f"🧮 Result: {eval(expression)}"
        except:
            return "❌ Invalid calculation"

    # ---------------- GREETING ----------------
    if "hello" in text or "hi" in text:
        return "Hey Gowtham 👋 I'm your AI agent!"

    # ---------------- NORMAL CHAT (OPTIMIZED) ----------------
    prompt = f"""
    You are a helpful AI assistant.

    Recent conversation:
    {chat_history[-3:]}   # 🔥 only last 3 messages

    User: {user_input}

    Give a short and clear answer.
    """

    return ask_llama(prompt)