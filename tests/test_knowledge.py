import pytest
from ai.knowledge import get_knowledge_base

def test_knowledge_base_overview():
    kb = get_knowledge_base()
    overview = kb.get_college_overview()
    assert "P. R. Pote Patil" in overview.get("name", "")
    assert overview.get("dte_code") == "1107"
    assert "NAAC" in overview.get("accreditation", "")

def test_knowledge_base_departments():
    kb = get_knowledge_base()
    depts = kb.get_departments()
    assert len(depts) >= 7
    
    cse = kb.get_department("cse")
    assert cse is not None
    assert "Gadicha" in cse.get("hod", "")
    assert cse.get("intake_btech") == 180

def test_knowledge_base_programs():
    kb = get_knowledge_base()
    progs = kb.get_programs()
    assert len(progs) >= 4
    deg_names = [p.get("degree") for p in progs]
    assert any("B.Tech" in d for d in deg_names)
    assert any("MBA" in d for d in deg_names)

def test_knowledge_base_admissions_and_fees():
    kb = get_knowledge_base()
    admissions = kb.get_admission_info()
    assert "CAP" in admissions.get("admission_process", "")
    assert len(admissions.get("required_documents", [])) >= 10

    fees = kb.get_fee_info()
    assert len(fees.get("scholarships", [])) >= 3

def test_knowledge_base_facilities_and_sources():
    kb = get_knowledge_base()
    lib = kb.get_facility("library")
    assert lib is not None
    assert "35,000+" in lib.get("description", "")

    sources = kb.get_sources()
    assert len(sources) >= 5

def test_knowledge_search():
    kb = get_knowledge_base()
    res = kb.search_knowledge("Computer Engineering")
    assert len(res) > 0
