import pytest
from ai.rules import reason_with_rules

def test_greeting_rule():
    decision = reason_with_rules("greeting", 0.95, {})
    assert decision["action"] == "RESPOND_GREETING"
    assert decision["rule"] == "rule_greeting"

def test_hod_specific_rule():
    decision = reason_with_rules("hod", 0.92, {"department": "cse"})
    assert decision["action"] == "LOOKUP_HOD"
    assert decision["department"] == "cse"

def test_admission_rule():
    decision = reason_with_rules("admission", 0.88, {})
    assert decision["action"] == "LOOKUP_ADMISSION_PROCESS"

def test_documents_rule():
    decision = reason_with_rules("documents", 0.85, {})
    assert decision["action"] == "LOOKUP_DOCUMENTS"
