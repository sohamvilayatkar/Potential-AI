import pytest
from ai.entities import extract_entities

def test_extract_department_entities():
    res_cse = extract_entities("Who is the HOD of Computer Science and Engineering?")
    assert res_cse["department"] == "cse"
    assert "Computer Science" in res_cse["department_name"]

    res_aiml = extract_entities("Tell me about CSE AIML branch")
    assert res_aiml["department"] == "cse_aiml"

    res_aids = extract_entities("What is the intake for artificial intelligence and data science?")
    assert res_aids["department"] == "aids"

    res_me = extract_entities("Show me laboratories in mechanical engineering")
    assert res_me["department"] == "me"

    res_ee = extract_entities("Who heads electrical engineering department?")
    assert res_ee["department"] == "ee"

    res_extc = extract_entities("Tell me about EXTC department")
    assert res_extc["department"] == "extc"

def test_extract_program_entities():
    res_btech = extract_entities("What is the admission criteria for B.Tech degree?")
    assert res_btech["program"] == "btech"

    res_mtech = extract_entities("What is the eligibility for M.Tech programs?")
    assert res_mtech["program"] == "mtech"

    res_mba = extract_entities("How many seats in MBA?")
    assert res_mba["program"] == "mba"

    res_mca = extract_entities("Tell me about MCA admission")
    assert res_mca["program"] == "mca"

def test_extract_academic_year():
    res_25 = extract_entities("What is the fee structure for 2025-26?")
    assert res_25["academic_year"] == "2025-26"

    res_26 = extract_entities("Show me admission rules for 2026-27")
    assert res_26["academic_year"] == "2026-27"

def test_extract_info_types():
    assert extract_entities("Who is the HOD?")["info_type"] == "hod"
    assert extract_entities("What are the fees?")["info_type"] == "fees"
    assert extract_entities("What is the admission procedure?")["info_type"] == "admission"
    assert extract_entities("What documents are required?")["info_type"] == "documents"
    assert extract_entities("Where is the central library?")["info_type"] == "library"
    assert extract_entities("Is hostel facility available?")["info_type"] == "hostel"

def test_extract_no_false_positives():
    res = extract_entities("What is the theory of relativity?")
    assert res["department"] is None
    assert res["program"] is None
