from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from agent import ai_agent, load_pdf

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(data: dict):
    user_msg = data.get("message")
    reply = ai_agent(user_msg)
    return {"reply": reply}

# ---------------- PDF ----------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    load_pdf(file_path)

    return {"reply": "PDF uploaded and ready ✅"}