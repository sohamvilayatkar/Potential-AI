"""
Intent Classification Module using TF-IDF and Logistic Regression.
Trains on data/intents.csv and predicts user intent with probability confidence.
"""

import os
import pickle
import numpy as np
from typing import Tuple, Dict, Any, Optional
from ai.preprocess import preprocess_query

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "intent_model.pkl")

class IntentClassifier:
    def __init__(self, vectorizer_path: str = VECTORIZER_PATH, model_path: str = MODEL_PATH):
        self.vectorizer_path = vectorizer_path
        self.model_path = model_path
        self.vectorizer = None
        self.model = None
        self.is_loaded = False
        self.load_model()

    def load_model(self) -> bool:
        """Load trained vectorizer and model from disk."""
        if os.path.exists(self.vectorizer_path) and os.path.exists(self.model_path):
            try:
                with open(self.vectorizer_path, "rb") as vf:
                    self.vectorizer = pickle.load(vf)
                with open(self.model_path, "rb") as mf:
                    self.model = pickle.load(mf)
                self.is_loaded = True
                return True
            except Exception as e:
                print(f"[Classifier] Error loading models: {e}")
                self.is_loaded = False
                return False
        else:
            self.is_loaded = False
            return False

    def predict(self, query: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict user intent from text query.
        Returns: (predicted_intent, confidence, all_probabilities)
        """
        if not self.is_loaded or self.vectorizer is None or self.model is None:
            # Fallback if model not trained yet
            return ("fallback", 0.0, {})

        processed = preprocess_query(query)
        if not processed.strip():
            return ("fallback", 0.0, {})

        try:
            vec = self.vectorizer.transform([processed])
            probs = self.model.predict_proba(vec)[0]
            classes = self.model.classes_

            best_idx = np.argmax(probs)
            predicted_intent = classes[best_idx]
            confidence = float(probs[best_idx])

            prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
            return (predicted_intent, confidence, prob_dict)
        except Exception as e:
            print(f"[Classifier] Error during prediction: {e}")
            return ("fallback", 0.0, {})

# Global singleton classifier instance for application reuse
_classifier_instance: Optional[IntentClassifier] = None

def get_classifier() -> IntentClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier()
    return _classifier_instance
