from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from google import genai
from google.genai import types

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()
@app.get("/")
def root():
    return {"status": "Backend is running"}


@app.post("/api/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return {"pdf_text": text}

@app.post("/api/chat")
async def chat(message: str, pdf_content: str):
    pdf_lines = pdf_content.splitlines()
    pdf_context = "\n".join(pdf_lines[:250])
    prompt = f"Context: {pdf_context}\nQuestion: {message}"
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt]
    )
    return {"response": response.text}
