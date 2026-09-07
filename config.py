"""
Configuration settings for Potential AI College Assistant.
Loads environment variables and sets production/development parameters.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "potential-ai-prpcem-secret-key-2026")
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5002))
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]

    # AI Model & Confidence Parameters
    CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.35))
    INTENT_CONFIDENCE_THRESHOLD = CONFIDENCE_THRESHOLD
    
    # File Paths
    DATA_DIR = os.path.join(BASE_DIR, "data")
    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "college_data.json")
    SOURCES_PATH = os.path.join(DATA_DIR, "sources.json")
    INTENTS_PATH = os.path.join(DATA_DIR, "intents.csv")
    DB_PATH = os.path.join(DATA_DIR, "potential_ai.db")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
    MODEL_PATH = os.path.join(MODELS_DIR, "intent_model.pkl")
    METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

    # College Branding
    COLLEGE_NAME = "P. R. Pote Patil College of Engineering & Management, Amravati"
    BOT_NAME = "Potential AI"
    TAGLINE = "Intelligent College Assistant"

    # Telegram Bot Integration
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8630475971:AAGeWCoEhCQc3SxRKzN8pNSUTkp2n8bUgTs")
    TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME", "PRPCEM_PotentialAI_Bot")
