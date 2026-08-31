import pytest
from ai.response import get_response_generator

def test_chatbot_factual_responses():
    rg = get_response_generator()

    # 1. Leadership: Principal
    res_p = rg.generate_response("Who is the principal?")
    assert "Jawandhiya" in res_p["response"]
    assert res_p["intent"] == "principal"
    assert len(res_p["sources"]) > 0

    # 2. Leadership: Chairman
    res_c = rg.generate_response("Who is the chairman?")
    assert "Pravinkumar" in res_c["response"]
    assert res_c["intent"] == "chairman"
    assert len(res_c["sources"]) > 0

    # 3. Leadership: Dean Academics
    res_d = rg.generate_response("Who is the dean of academics?")
    assert "Kute" in res_d["response"]
    assert res_d["intent"] == "dean"
    assert len(res_d["sources"]) > 0

    # 4. HOD CSE
    res_hod = rg.generate_response("Who is the HOD of Computer Engineering?")
    assert "Gadicha" in res_hod["response"] or "HOD" in res_hod["response"]
    assert res_hod["intent"] == "hod"
    assert len(res_hod["sources"]) > 0

    # 5. Admission Process
    res_adm = rg.generate_response("What is the admission process?")
    assert "CAP" in res_adm["response"] or "1107" in res_adm["response"]
    assert len(res_adm["sources"]) > 0

    # 6. Documents
    res_doc = rg.generate_response("What documents are required for admission?")
    assert "Marksheet" in res_doc["response"]
    assert len(res_doc["sources"]) > 0

    # 7. Library
    res_lib = rg.generate_response("Where is the library?")
    assert "Library" in res_lib["response"]

def test_chatbot_fallback_unrelated():
    rg = get_response_generator()
    res = rg.generate_response("What is quantum electrodynamics in astrophysics?")
    assert "couldn't find this specific information" in res["response"].lower()
    assert res["intent"] == "fallback"
