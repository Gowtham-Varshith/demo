# agent.py

import ollama

def ask_ai_stream(prompt, model="phi3"):
    """
    Streams response for fast UI updates
    """
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_text = ""
        for chunk in response:
            content = chunk["message"]["content"]
            full_text += content
            yield full_text

    except Exception as e:
        yield f"❌ Error: {e}"


# ---- FALLBACK (for cloud demo) ----
def fake_ai_response(prompt):
    return f"""
🤖 Demo Mode Response:

You asked: {prompt}

This is a simulated response for cloud demo.
Locally, this runs a real LLM using Ollama.
"""