"""
Experta Rule Engine for Potential AI.
Implements symbolic reasoning using Facts, Rules, KnowledgeEngine, and forward-chaining inference.
Maps predicted ML intent + extracted entities to structured knowledge retrieval actions.
"""

import os
import sys

# Collections compatibility shim for Python 3.10+ / 3.13+ support with Experta
import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Sequence'):
    collections.Sequence = collections.abc.Sequence
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

try:
    from experta import KnowledgeEngine, Rule, Fact, MATCH, AS, AND, OR, NOT, L, W, TEST
    EXPERTA_AVAILABLE = True
except Exception as e:
    print(f"[Experta Warning] Could not import experta directly: {e}. Fallback engine will be used.")
    EXPERTA_AVAILABLE = False
    # Minimal fallback dummy classes if needed
    class Fact(dict):
        def __init__(self, **kwargs):
            super().__init__(kwargs)
    class KnowledgeEngine:
        def reset(self): pass
        def declare(self, *facts): pass
        def run(self): pass
    def Rule(*args, **kwargs):
        def decorator(fn): return fn
        return decorator
    def TEST(fn): return fn
    MATCH = W = L = AS = AND = OR = NOT = None

# Define Knowledge Facts
class UserQuery(Fact):
    """Raw user message fact."""
    pass

class QueryIntent(Fact):
    """Predicted intent and confidence score from ML classifier."""
    pass

class ExtractedEntity(Fact):
    """Entities recognized from the query (department, program, info_type)."""
    pass

class CollegeAction(Fact):
    """Structured action output deduced by the rule engine."""
    pass

class PotentialAIRuleEngine(KnowledgeEngine):
    """
    Symbolic Rule-Based Inference Engine for PRPCEM College Assistant.
    Evaluates ML intent alongside entity context to select the most specific reasoning rule.
    """
    def __init__(self):
        super().__init__()
        self.selected_action = None
        self.fired_rules = []

    # 1. Greetings, Goodbye, Thanks
    @Rule(QueryIntent(intent='greeting'))
    def rule_greeting(self):
        self.fired_rules.append("rule_greeting")
        self.selected_action = {
            "action": "RESPOND_GREETING",
            "rule": "rule_greeting",
            "description": "User initiated conversation with a greeting."
        }

    @Rule(QueryIntent(intent='goodbye'))
    def rule_goodbye(self):
        self.fired_rules.append("rule_goodbye")
        self.selected_action = {
            "action": "RESPOND_GOODBYE",
            "rule": "rule_goodbye",
            "description": "User is parting/ending conversation."
        }

    @Rule(QueryIntent(intent='thanks'))
    def rule_thanks(self):
        self.fired_rules.append("rule_thanks")
        self.selected_action = {
            "action": "RESPOND_THANKS",
            "rule": "rule_thanks",
            "description": "User expressed gratitude."
        }

    # 1.1 Leadership & Administration: Principal, Chairman, Dean, Leadership
    @Rule(
        OR(
            QueryIntent(intent='principal'),
            ExtractedEntity(info_type='principal')
        ),
        salience=15
    )
    def rule_principal(self):
        self.fired_rules.append("rule_principal")
        self.selected_action = {
            "action": "LOOKUP_PRINCIPAL",
            "rule": "rule_principal",
            "description": "Retrieve information about the College Principal."
        }

    @Rule(
        OR(
            QueryIntent(intent='chairman'),
            ExtractedEntity(info_type='chairman')
        ),
        salience=15
    )
    def rule_chairman(self):
        self.fired_rules.append("rule_chairman")
        self.selected_action = {
            "action": "LOOKUP_CHAIRMAN",
            "rule": "rule_chairman",
            "description": "Retrieve information about the Founder & Chairman and Trust."
        }

    @Rule(
        OR(
            QueryIntent(intent='dean'),
            ExtractedEntity(info_type='dean')
        ),
        salience=15
    )
    def rule_dean(self):
        self.fired_rules.append("rule_dean")
        self.selected_action = {
            "action": "LOOKUP_DEAN",
            "rule": "rule_dean",
            "description": "Retrieve information about the Dean (Academics)."
        }

    @Rule(
        OR(
            QueryIntent(intent='leadership'),
            ExtractedEntity(info_type='leadership')
        ),
        salience=12
    )
    def rule_leadership(self):
        self.fired_rules.append("rule_leadership")
        self.selected_action = {
            "action": "LOOKUP_LEADERSHIP",
            "rule": "rule_leadership",
            "description": "Retrieve institutional governance and leadership team."
        }

    # 2. HOD Lookups - Department Specific vs General
    @Rule(
        AND(
            QueryIntent(intent='hod'),
            ExtractedEntity(department=MATCH.dept),
            TEST(lambda dept: dept is not None)
        ),
        salience=10
    )
    def rule_hod_specific_department(self, dept):
        self.fired_rules.append("rule_hod_specific_department")
        self.selected_action = {
            "action": "LOOKUP_HOD",
            "department": dept,
            "rule": "rule_hod_specific_department",
            "description": f"Specific HOD lookup for department: {dept}"
        }

    @Rule(
        AND(
            QueryIntent(intent='hod'),
            ExtractedEntity(department=None)
        ),
        salience=5
    )
    def rule_hod_all_departments(self):
        self.fired_rules.append("rule_hod_all_departments")
        self.selected_action = {
            "action": "LOOKUP_ALL_HODS",
            "rule": "rule_hod_all_departments",
            "description": "General lookup of all department heads."
        }

    # 3. Department Information
    @Rule(
        AND(
            QueryIntent(intent='departments'),
            ExtractedEntity(department=MATCH.dept),
            TEST(lambda dept: dept is not None)
        ),
        salience=10
    )
    def rule_department_specific(self, dept):
        self.fired_rules.append("rule_department_specific")
        self.selected_action = {
            "action": "LOOKUP_DEPARTMENT_DETAIL",
            "department": dept,
            "rule": "rule_department_specific",
            "description": f"Detailed info lookup for department {dept}"
        }

    @Rule(
        AND(
            QueryIntent(intent='departments'),
            ExtractedEntity(department=None)
        ),
        salience=5
    )
    def rule_department_list(self):
        self.fired_rules.append("rule_department_list")
        self.selected_action = {
            "action": "LOOKUP_ALL_DEPARTMENTS",
            "rule": "rule_department_list",
            "description": "Listing all engineering and PG departments."
        }

    # 4. Courses & Programs
    @Rule(QueryIntent(intent='courses'))
    def rule_courses(self):
        self.fired_rules.append("rule_courses")
        self.selected_action = {
            "action": "LOOKUP_COURSES",
            "rule": "rule_courses",
            "description": "Retrieve undergraduate and postgraduate degree courses."
        }

    @Rule(
        AND(
            QueryIntent(intent='programs'),
            ExtractedEntity(program=MATCH.prog),
            TEST(lambda prog: prog is not None)
        ),
        salience=10
    )
    def rule_program_specific(self, prog):
        self.fired_rules.append("rule_program_specific")
        self.selected_action = {
            "action": "LOOKUP_PROGRAM_DETAIL",
            "program": prog,
            "rule": "rule_program_specific",
            "description": f"Retrieve details for program: {prog}"
        }

    @Rule(
        AND(
            QueryIntent(intent='programs'),
            ExtractedEntity(program=None)
        ),
        salience=5
    )
    def rule_program_all(self):
        self.fired_rules.append("rule_program_all")
        self.selected_action = {
            "action": "LOOKUP_ALL_PROGRAMS",
            "rule": "rule_program_all",
            "description": "Retrieve all B.Tech, M.Tech, MBA, MCA programs."
        }

    # 5. Admission, Eligibility & Required Documents
    @Rule(QueryIntent(intent='admission'))
    def rule_admission(self):
        self.fired_rules.append("rule_admission")
        self.selected_action = {
            "action": "LOOKUP_ADMISSION_PROCESS",
            "rule": "rule_admission",
            "description": "Retrieve CAP admission procedure, DTE code 1107, and timeline."
        }

    @Rule(QueryIntent(intent='eligibility'))
    def rule_eligibility(self):
        self.fired_rules.append("rule_eligibility")
        self.selected_action = {
            "action": "LOOKUP_ELIGIBILITY",
            "rule": "rule_eligibility",
            "description": "Retrieve HSC / CET / GATE / DSE eligibility criteria."
        }

    @Rule(QueryIntent(intent='documents'))
    def rule_documents(self):
        self.fired_rules.append("rule_documents")
        self.selected_action = {
            "action": "LOOKUP_DOCUMENTS",
            "rule": "rule_documents",
            "description": "Retrieve official admission documents checklist."
        }

    # 6. Fees, Scholarships & Intake
    @Rule(QueryIntent(intent='fees'))
    def rule_fees(self):
        self.fired_rules.append("rule_fees")
        self.selected_action = {
            "action": "LOOKUP_FEES",
            "rule": "rule_fees",
            "description": "Retrieve FRA sanctioned tuition fees and category concessions."
        }

    @Rule(QueryIntent(intent='scholarship'))
    def rule_scholarship(self):
        self.fired_rules.append("rule_scholarship")
        self.selected_action = {
            "action": "LOOKUP_SCHOLARSHIPS",
            "rule": "rule_scholarship",
            "description": "Retrieve MahaDBT, EBC, SC/ST/OBC, and TFWS schemes."
        }

    @Rule(
        AND(
            QueryIntent(intent='intake'),
            ExtractedEntity(department=MATCH.dept),
            TEST(lambda dept: dept is not None)
        ),
        salience=10
    )
    def rule_intake_dept(self, dept):
        self.fired_rules.append("rule_intake_dept")
        self.selected_action = {
            "action": "LOOKUP_INTAKE_DEPT",
            "department": dept,
            "rule": "rule_intake_dept",
            "description": f"Seat capacity lookup for department {dept}"
        }

    @Rule(
        AND(
            QueryIntent(intent='intake'),
            ExtractedEntity(department=None)
        ),
        salience=5
    )
    def rule_intake_all(self):
        self.fired_rules.append("rule_intake_all")
        self.selected_action = {
            "action": "LOOKUP_INTAKE_ALL",
            "rule": "rule_intake_all",
            "description": "Overall B.Tech and PG seat intake overview."
        }

    # 7. Campus Facilities
    @Rule(QueryIntent(intent='library'))
    def rule_library(self):
        self.fired_rules.append("rule_library")
        self.selected_action = {
            "action": "LOOKUP_LIBRARY",
            "rule": "rule_library",
            "description": "Retrieve Central Library volume count, DELNET, and reading hours."
        }

    @Rule(QueryIntent(intent='hostel'))
    def rule_hostel(self):
        self.fired_rules.append("rule_hostel")
        self.selected_action = {
            "action": "LOOKUP_HOSTEL",
            "rule": "rule_hostel",
            "description": "Retrieve Boys/Girls Hostel amenities, security, and mess details."
        }

    @Rule(QueryIntent(intent='facilities'))
    def rule_facilities(self):
        self.fired_rules.append("rule_facilities")
        self.selected_action = {
            "action": "LOOKUP_FACILITIES",
            "rule": "rule_facilities",
            "description": "Retrieve complete campus infrastructure and student amenities."
        }

    @Rule(QueryIntent(intent='laboratories'))
    def rule_laboratories(self):
        self.fired_rules.append("rule_laboratories")
        self.selected_action = {
            "action": "LOOKUP_LABORATORIES",
            "rule": "rule_laboratories",
            "description": "Retrieve department practical labs and research computing centers."
        }

    # 8. Academics, Syllabus, Calendar, Exams, Notices
    @Rule(QueryIntent(intent='academic_calendar'))
    def rule_academic_calendar(self):
        self.fired_rules.append("rule_academic_calendar")
        self.selected_action = {
            "action": "LOOKUP_ACADEMIC_CALENDAR",
            "rule": "rule_academic_calendar",
            "description": "Retrieve teaching timeline and semester start/end schedule."
        }

    @Rule(QueryIntent(intent='syllabus'))
    def rule_syllabus(self):
        self.fired_rules.append("rule_syllabus")
        self.selected_action = {
            "action": "LOOKUP_SYLLABUS",
            "rule": "rule_syllabus",
            "description": "Retrieve autonomous course scheme and syllabus links."
        }

    @Rule(QueryIntent(intent='examination'))
    def rule_examination(self):
        self.fired_rules.append("rule_examination")
        self.selected_action = {
            "action": "LOOKUP_EXAMINATION",
            "rule": "rule_examination",
            "description": "Retrieve exam registration portal and end-semester rules."
        }

    @Rule(QueryIntent(intent='notices'))
    def rule_notices(self):
        self.fired_rules.append("rule_notices")
        self.selected_action = {
            "action": "LOOKUP_NOTICES",
            "rule": "rule_notices",
            "description": "Retrieve official latest academic circulars and announcements."
        }

    # 9. General College Information, History, Vision/Mission
    @Rule(QueryIntent(intent='college_information'))
    def rule_college_information(self):
        self.fired_rules.append("rule_college_information")
        self.selected_action = {
            "action": "LOOKUP_COLLEGE_OVERVIEW",
            "rule": "rule_college_information",
            "description": "Retrieve PRPCEM overview, trust, leadership, and approvals."
        }

    @Rule(QueryIntent(intent='history'))
    def rule_history(self):
        self.fired_rules.append("rule_history")
        self.selected_action = {
            "action": "LOOKUP_HISTORY",
            "rule": "rule_history",
            "description": "Retrieve establishment year 2009 and institutional growth history."
        }

    @Rule(QueryIntent(intent='vision_mission'))
    def rule_vision_mission(self):
        self.fired_rules.append("rule_vision_mission")
        self.selected_action = {
            "action": "LOOKUP_VISION_MISSION",
            "rule": "rule_vision_mission",
            "description": "Retrieve institutional vision, mission, and quality policy."
        }

    # 10. Contact, Location, Autonomy, Accreditation, Placement
    @Rule(QueryIntent(intent='contact'))
    def rule_contact(self):
        self.fired_rules.append("rule_contact")
        self.selected_action = {
            "action": "LOOKUP_CONTACT",
            "rule": "rule_contact",
            "description": "Retrieve phone numbers, principal email, and working hours."
        }

    @Rule(QueryIntent(intent='location'))
    def rule_location(self):
        self.fired_rules.append("rule_location")
        self.selected_action = {
            "action": "LOOKUP_LOCATION",
            "rule": "rule_location",
            "description": "Retrieve campus postal address on Kathora Road, Amravati."
        }

    @Rule(QueryIntent(intent='autonomy'))
    def rule_autonomy(self):
        self.fired_rules.append("rule_autonomy")
        self.selected_action = {
            "action": "LOOKUP_AUTONOMY",
            "rule": "rule_autonomy",
            "description": "Retrieve autonomous status, academic regulations, and SGBAU affiliation."
        }

    @Rule(QueryIntent(intent='accreditation'))
    def rule_accreditation(self):
        self.fired_rules.append("rule_accreditation")
        self.selected_action = {
            "action": "LOOKUP_ACCREDITATION",
            "rule": "rule_accreditation",
            "description": "Retrieve NAAC Grade A (CGPA 3.07), AICTE approval, DTE Code 1107."
        }

    @Rule(QueryIntent(intent='placement'))
    def rule_placement(self):
        self.fired_rules.append("rule_placement")
        self.selected_action = {
            "action": "LOOKUP_PLACEMENT",
            "rule": "rule_placement",
            "description": "Retrieve Training & Placement cell details and campus recruiter MOUs."
        }

    @Rule(QueryIntent(intent='faculty'))
    def rule_faculty(self):
        self.fired_rules.append("rule_faculty")
        self.selected_action = {
            "action": "LOOKUP_FACULTY",
            "rule": "rule_faculty",
            "description": "Retrieve academic faculty and leadership information."
        }

def reason_with_rules(intent: str, confidence: float, entities: dict, query_text: str = "") -> dict:
    """
    Runs the Experta inference engine given the ML predicted intent and extracted entities.
    Returns the action recommendation dictionary.
    """
    engine = PotentialAIRuleEngine()
    engine.reset()

    # Declare facts
    engine.declare(UserQuery(text=query_text))
    engine.declare(QueryIntent(intent=intent, confidence=confidence))
    engine.declare(ExtractedEntity(
        department=entities.get("department"),
        department_name=entities.get("department_name"),
        program=entities.get("program"),
        info_type=entities.get("info_type")
    ))

    engine.run()

    if engine.selected_action:
        return engine.selected_action
    else:
        return {
            "action": "FALLBACK",
            "rule": "default_fallback",
            "description": "No explicit symbolic rule triggered; routing to fallback response."
        }
