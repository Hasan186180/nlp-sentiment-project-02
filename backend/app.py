#backend/app.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = FastAPI(title="AI Sentiment Analysis API")

# Lazy-loaded tokenizer and model to avoid hard failures at import time
tokenizer = None
model = None

# Fallback default key if not present in env
API_KEY = os.getenv("API_KEY", "sentiment_analysis_secure_key_2026")

class TextRequest(BaseModel):
    text: str


def load_model():
    """Load tokenizer and model into module-level variables.
    Tries local directory 'model_turkish' first, then falls back to Hugging Face Hub.
    """
    global tokenizer, model
    model_dir = os.path.join(os.path.dirname(__file__), "model_turkish")
    
    # Check if local directory exists and contains files
    local_exists = False
    if os.path.isdir(model_dir):
        files = os.listdir(model_dir)
        if len(files) > 0:
            local_exists = True
            
    if not local_exists:
        model_dir = "azizbarank/distilbert-base-turkish-cased-sentiment"
        logging.info(f"Local model not found. Falling back to Hugging Face Hub: {model_dir}")
    else:
        logging.info(f"Loading model from local directory: {model_dir}")
        
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        logging.info("Model and tokenizer loaded successfully")
    except Exception:
        logging.exception("Failed to load model/tokenizer")
        tokenizer = None
        model = None


@app.on_event("startup")
def on_startup():
    load_model()


@app.post("/predict")
def predict(
    request: TextRequest,
    x_api_key: str = Header(...)
):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if tokenizer is None or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Check server logs for details."
        )

    inputs = tokenizer(
        request.text,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)

    return {
        "negative": float(probs[0][0]),
        "positive": float(probs[0][1])
    }