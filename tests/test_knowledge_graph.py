import pytest
from ai.knowledge_graph import get_knowledge_graph

def test_knowledge_graph_structure():
    kg = get_knowledge_graph()
    assert kg.graph.number_of_nodes() >= 30
    assert kg.graph.number_of_edges() >= 30
    assert "PRPCEM" in kg.graph

def test_hod_lookup():
    kg = get_knowledge_graph()
    cse_hod = kg.get_hod("cse")
    assert cse_hod is not None

    all_hods = kg.get_all_hods()
    assert len(all_hods) >= 7

def test_leadership_lookup():
    kg = get_knowledge_graph()
    principal = kg.get_principal()
    assert "Jawandhiya" in principal.get("name", "")

    chairman = kg.get_chairman()
    assert "Pravinkumar" in chairman.get("founder_chairman", "")

    dean = kg.get_dean()
    assert "Kute" in dean.get("name", "")

def test_facility_lookup():
    kg = get_knowledge_graph()
    library = kg.get_facility_info("Library")
    assert library is not None
    assert "Central Library" in library["name"]
