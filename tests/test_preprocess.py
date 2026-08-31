import pytest
from ai.preprocess import clean_text, tokenize, preprocess_query, extract_entities

def test_clean_text():
    raw = "Hello! Tell me about PRPCEM's Courses...   "
    cleaned = clean_text(raw)
    assert "hello" in cleaned
    assert "prpcem" in cleaned
    assert "courses" in cleaned
    assert "!" not in cleaned

def test_tokenize():
    tokens = tokenize("What is the fee structure?")
    assert "what" in tokens
    assert "fee" in tokens
    assert "structure" in tokens

def test_extract_entities():
    e_cse = extract_entities("Who is the HOD of Computer Engineering?")
    assert e_cse["department"] == "cse"

    e_me = extract_entities("Tell me about mechanical engineering")
    assert e_me["department"] == "me"

    e_btech = extract_entities("What is the eligibility for btech admission?")
    assert e_btech["program"] == "btech"

    # Should not match 'me' inside unrelated words
    e_unrelated = extract_entities("What is electrodynamics in physics?")
    assert e_unrelated["department"] is None
