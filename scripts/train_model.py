"""
Training Script for Potential AI Intent Classifier.
Loads training data from data/intents.csv, trains TF-IDF and Logistic Regression,
evaluates performance metrics, and saves model artifacts and metadata to models/.
"""

import os
import sys
import pickle
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

from ai.preprocess import preprocess_query

DATA_PATH = os.path.join(BASE_DIR, "data", "intents.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "intent_model.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

def train_intent_classifier():
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("==================================================")
    print("      POTENTIAL AI - INTENT MODEL TRAINING        ")
    print("==================================================")
    
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Training dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    total_examples = len(df)
    unique_intents = sorted(df['intent'].unique().tolist())
    print(f"Loaded {total_examples} training examples across {len(unique_intents)} unique intents.")
    
    # Preprocess text
    df['clean_text'] = df['text'].apply(preprocess_query)
    
    X = df['clean_text']
    y = df['intent']

    # Train / Test split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training Set: {len(X_train)} samples | Test Set: {len(X_test)} samples")

    # Fit TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    vocab_size = len(vectorizer.vocabulary_)
    print(f"Vocabulary Size: {vocab_size} features")

    # Train Logistic Regression Model
    classifier = LogisticRegression(
        C=10.0,
        max_iter=1000,
        class_weight='balanced',
        random_state=42
    )
    classifier.fit(X_train_vec, y_train)

    # Evaluate on Test Set
    y_pred = classifier.predict(X_test_vec)
    acc = float(accuracy_score(y_test, y_pred))
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
    prec = float(prec)
    rec = float(rec)
    f1 = float(f1)

    print("\n---------------- MODEL EVALUATION METRICS ----------------")
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
    print("----------------------------------------------------------\n")

    # Retrain on full dataset for maximum production accuracy
    X_full_vec = vectorizer.fit_transform(X)
    classifier.fit(X_full_vec, y)

    # Save artifacts
    with open(VECTORIZER_PATH, "wb") as vf:
        pickle.dump(vectorizer, vf)
    with open(MODEL_PATH, "wb") as mf:
        pickle.dump(classifier, mf)

    metadata = {
        "model_name": "TF-IDF + Logistic Regression Intent Classifier",
        "algorithm": "LogisticRegression",
        "vectorizer": "TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True)",
        "hyperparameters": {
            "C": 10.0,
            "max_iter": 1000,
            "class_weight": "balanced",
            "random_state": 42
        },
        "evaluation_metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4)
        },
        "dataset_statistics": {
            "total_samples": total_examples,
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "vocabulary_size": vocab_size,
            "num_intents": len(unique_intents),
            "intents": unique_intents
        },
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as json_f:
        json.dump(metadata, json_f, indent=4)

    print(f"Saved TF-IDF Vectorizer to: {VECTORIZER_PATH}")
    print(f"Saved Intent Model to:      {MODEL_PATH}")
    print(f"Saved Model Metadata to:    {METADATA_PATH}")
    print("Model training completed successfully!")

if __name__ == "__main__":
    train_intent_classifier()
