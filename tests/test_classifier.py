import pytest
from ai.classifier import get_classifier

def test_classifier_loaded():
    classifier = get_classifier()
    assert classifier.is_loaded is True
    assert classifier.vectorizer is not None
    assert classifier.model is not None

def test_predict_intents():
    classifier = get_classifier()
    
    intent, conf, _ = classifier.predict("What courses are offered?")
    assert intent == "courses"
    assert conf > 0.40

    intent, conf, _ = classifier.predict("Who is the HOD of computer science?")
    assert intent == "hod"
    assert conf > 0.40

    intent, conf, _ = classifier.predict("What is the admission procedure?")
    assert intent == "admission"
    assert conf > 0.40
