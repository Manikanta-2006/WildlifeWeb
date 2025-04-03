from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from typing import Dict
from io import BytesIO

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google AI
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Pydantic models
class ChatMessage(BaseModel):
    message: str


# Root endpoint
@app.get("/")
@app.head("/")
async def read_root():
    return {"message": "API is working!"}

# CORS pre-flight handlers
@app.options("/api/chat/")
async def handle_options_chat():
    return JSONResponse(content={}, status_code=200)


# Chat endpoint
@app.post("/api/chat")
async def chat(message: ChatMessage) -> Dict[str, str]:
    prompt = f"""
    You are a wildlife AI assistant. Provide Act as a wildlife guide and tell about animals also
    
    User question: {message.message}
    """
    
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing the request: {str(e)}")

