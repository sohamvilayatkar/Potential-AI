"""
Response Generation Module for Potential AI.
Synthesizes ML intent, entity extraction, Experta symbolic inference,
NetworkX knowledge graph queries, and official JSON records into accurate,
source-attributed responses.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from ai.preprocess import clean_text, extract_entities
from ai.classifier import get_classifier
from ai.rules import reason_with_rules
from ai.knowledge_graph import get_knowledge_graph

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "college_data.json")

# Configurable confidence threshold
DEFAULT_CONFIDENCE_THRESHOLD = 0.35

FALLBACK_MESSAGE = (
    "I couldn't find this specific information in the official PRPCEM knowledge base. "
    "Please check the official college website (https://prpotepatilengg.ac.in/) or the "
    "academic portal (https://academics.prpotepatilengg.ac.in/) for the latest updates."
)

FALLBACK_SUGGESTIONS = (
    "You can ask me about courses, departments, admissions, faculty, fees, "
    "facilities, scholarships, library, hostel, academic calendar, or college contact details."
)

class ResponseGenerator:
    def __init__(self, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        self.classifier = get_classifier()
        self.kg = get_knowledge_graph()
        self.college_data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                self.college_data = json.load(f)

    def generate_response(self, user_query: str) -> Dict[str, Any]:
        """
        Full 12-step AI response generation pipeline:
        1. Input validation
        2. NLP Preprocessing & cleaning
        3. Entity extraction
        4. TF-IDF vectorization & ML intent classification
        5. Confidence score evaluation
        6. Experta forward-chaining rule inference
        7. NetworkX semantic graph lookup
        8. Knowledge base factual retrieval
        9. Academic year verification
        10. Natural language synthesis
        11. Source attribution formatting
        12. Return structured JSON payload
        """
        # Step 1: Input Validation
        if not user_query or not user_query.strip():
            return {
                "response": "Please enter a question about P. R. Pote Patil College of Engineering & Management.",
                "intent": "empty_query",
                "confidence": 1.0,
                "sources": [],
                "academic_year": None,
                "ai_details": {
                    "intent": "empty_query",
                    "confidence_score": 1.0,
                    "entities": {},
                    "experta_rule": "none",
                    "reasoning_action": "EMPTY_INPUT",
                    "knowledge_engine": "Validation Filter"
                }
            }

        # Step 2 & 3: NLP Preprocessing & Entity Extraction
        cleaned_query = clean_text(user_query)
        entities = extract_entities(user_query)

        # Step 4 & 5: ML Intent Classification & Confidence
        intent, confidence, all_probs = self.classifier.predict(user_query)

        # Check for fallback threshold
        if confidence < self.confidence_threshold and not entities.get("department") and not entities.get("program"):
            return {
                "response": f"{FALLBACK_MESSAGE}\n\n{FALLBACK_SUGGESTIONS}",
                "intent": "fallback",
                "confidence": round(confidence, 4),
                "sources": [{
                    "title": "PRPCEM Official Website",
                    "url": "https://prpotepatilengg.ac.in/"
                }],
                "academic_year": "2025-26",
                "ai_details": {
                    "intent": intent,
                    "confidence_score": round(confidence, 4),
                    "entities": entities,
                    "experta_rule": "rule_low_confidence_fallback",
                    "reasoning_action": "FALLBACK",
                    "knowledge_engine": "Confidence Thresholding"
                }
            }

        # Step 6: Experta Symbolic Rule Reasoning
        action_decision = reason_with_rules(intent, confidence, entities, user_query)
        action = action_decision.get("action", "FALLBACK")
        rule_name = action_decision.get("rule", "unknown_rule")

        # Step 7, 8, 9: Knowledge Retrieval via Graph & Knowledge Base
        response_text, sources, academic_year = self._execute_action(action, action_decision, entities)

        return {
            "response": response_text,
            "intent": intent,
            "confidence": round(confidence, 4),
            "sources": sources,
            "academic_year": academic_year,
            "ai_details": {
                "intent": intent,
                "confidence_score": round(confidence, 4),
                "entities": entities,
                "experta_rule": rule_name,
                "reasoning_action": action,
                "knowledge_engine": "NetworkX + Experta Rule Engine"
            }
        }

    def _execute_action(self, action: str, action_data: dict, entities: dict) -> tuple:
        college = self.college_data.get("college", {})
        default_source = [{
            "title": college.get("source_title", "PRPCEM Official Website"),
            "url": college.get("source_url", "https://prpotepatilengg.ac.in/")
        }]

        # 1. Greetings / Goodbye / Thanks
        if action == "RESPOND_GREETING":
            return (
                "Hello! I am **Potential AI**, your intelligent college assistant for **P. R. Pote Patil College of Engineering & Management, Amravati**.\n\n"
                "How can I assist you today? You can ask me about:\n"
                "• **Courses & Programs** (B.Tech, M.Tech, MBA, MCA)\n"
                "• **Departments & HODs**\n"
                "• **Admission Process & Eligibility**\n"
                "• **Fees & Scholarships** (MahaDBT, EBC, TFWS)\n"
                "• **Campus Facilities** (Central Library, Hostels, Labs, Transport)\n"
                "• **Academic Calendars & Syllabus**",
                default_source,
                "2025-26"
            )

        if action == "RESPOND_GOODBYE":
            return (
                "Thank you for contacting Potential AI. If you have further queries about PRPCEM, feel free to ask anytime. Have a great day!",
                default_source,
                "2025-26"
            )

        if action == "RESPOND_THANKS":
            return (
                "You're very welcome! I'm glad I could help. Let me know if you need any other information regarding PRPCEM.",
                default_source,
                "2025-26"
            )

        # 1.1 Leadership & Administration Lookups
        if action == "LOOKUP_PRINCIPAL":
            principal = college.get("principal", "Dr. P. M. Jawandhiya")
            resp = (
                f"The Principal of **P. R. Pote Patil College of Engineering & Management (PRPCEM)** is **{principal}**.\n\n"
                f"• **Institution:** {college.get('name', 'PRPCEM, Amravati')}\n"
                f"• **Status:** Autonomous Institute (NAAC 'A' Grade)\n"
                f"• **Office Contact Email:** {self.college_data.get('contact', {}).get('emails', {}).get('principal', 'prpotepatilengg@gmail.com')}"
            )
            src = [{
                "title": "PRPCEM About Us & Leadership",
                "url": "https://prpotepatilengg.ac.in/about-college"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_CHAIRMAN":
            founder = college.get("founder_chairman", "Shri Pravinkumar R. Pote Patil (Former Minister of State, Govt. of Maharashtra)")
            vice = college.get("vice_chairman", "Shri Shreyash P. Pote")
            trust = college.get("trust", "P. R. Pote (Patil) Education & Welfare Trust")
            resp = (
                f"### Founder & Chairman of PRPCEM\n\n"
                f"• **Founder & Chairman:** **{founder}**\n"
                f"• **Vice-Chairman:** **{vice}**\n"
                f"• **Governing Trust:** {trust}\n"
                f"• **Establishment:** Established in {college.get('established_year', 2009)} at Pote Estate, Kathora Road, Amravati."
            )
            src = [{
                "title": "PRPCEM Trust & Governance",
                "url": "https://prpotepatilengg.ac.in/about-college"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_DEAN":
            dean = college.get("dean_academics", "Dr. V. B. Kute")
            resp = (
                f"The Dean (Academics) of **PRPCEM** is **{dean}**.\n\n"
                f"• **Office:** Office of Dean (Academics), Autonomous PRPCEM\n"
                f"• **Responsibilities:** Autonomous curriculum, academic calendar, ordinances, syllabus schemes, and examination coordination.\n"
                f"• **Dean Office Email:** {self.college_data.get('contact', {}).get('emails', {}).get('dean_academics', 'dean_acad@prpotepatilengg.ac.in')}"
            )
            src = [{
                "title": "Office of Dean (Academics) Official Portal",
                "url": "https://academics.prpotepatilengg.ac.in/"
            }]
            return (resp, src, "2026-27")

        if action == "LOOKUP_LEADERSHIP":
            founder = college.get("founder_chairman", "Shri Pravinkumar R. Pote Patil")
            vice = college.get("vice_chairman", "Shri Shreyash P. Pote")
            principal = college.get("principal", "Dr. P. M. Jawandhiya")
            dean = college.get("dean_academics", "Dr. V. B. Kute")
            resp = (
                f"### Key Leadership & Governance at PRPCEM\n\n"
                f"• **Founder & Chairman:** {founder}\n"
                f"• **Vice-Chairman:** {vice}\n"
                f"• **Principal:** {principal}\n"
                f"• **Dean (Academics):** {dean}\n"
                f"• **Governing Trust:** {college.get('trust', 'P. R. Pote (Patil) Education & Welfare Trust')}\n"
                f"• **Campus:** Pote Estate, Kathora Road, Amravati (Maharashtra)"
            )
            src = [{
                "title": "PRPCEM Leadership & Administration",
                "url": "https://prpotepatilengg.ac.in/about-college"
            }]
            return (resp, src, "2025-26")

        # 2. HOD Lookups (via NetworkX Graph)
        if action == "LOOKUP_HOD":
            dept_id = action_data.get("department") or entities.get("department")
            dept_info = self.kg.get_department_info(dept_id)
            if dept_info:
                dept_name = dept_info.get("name", dept_id)
                hod_name = dept_info.get("hod", "Not specified")
                resp = f"The Head of the Department (HOD) of **{dept_name}** is **{hod_name}**."
                src = [{
                    "title": f"PRPCEM {dept_name} Department Portal",
                    "url": dept_info.get("source_url") or "https://prpotepatilengg.ac.in/"
                }]
                return (resp, src, "2025-26")

        if action == "LOOKUP_ALL_HODS":
            hods = self.kg.get_all_hods()
            lines = ["**Heads of Departments (HODs) at PRPCEM:**\n"]
            for h in hods:
                lines.append(f"• **{h['department_name']}**: {h['hod']}")
            return ("\n".join(lines), default_source, "2025-26")

        # 3. Department details
        if action == "LOOKUP_DEPARTMENT_DETAIL":
            dept_id = action_data.get("department") or entities.get("department")
            for dept in self.college_data.get("departments", []):
                if dept["id"] == dept_id:
                    labs_str = ", ".join(dept.get("laboratories", []))
                    resp = (
                        f"### Department of {dept['name']} ({dept['short_name']})\n\n"
                        f"• **Head of Department (HOD):** {dept.get('hod')}\n"
                        f"• **B.Tech Seat Intake:** {dept.get('intake_btech', 'N/A')} seats\n"
                        f"• **Established Year:** {dept.get('established', '2009')}\n"
                        f"• **Overview:** {dept.get('description')}\n"
                        f"• **Laboratories:** {labs_str}"
                    )
                    src = [{
                        "title": dept.get("source_title", "PRPCEM Department Page"),
                        "url": dept.get("source_url", "https://prpotepatilengg.ac.in/")
                    }]
                    return (resp, src, dept.get("academic_year", "2025-26"))

        if action == "LOOKUP_ALL_DEPARTMENTS":
            departments = self.college_data.get("departments", [])
            lines = ["**Departments at P. R. Pote Patil College of Engineering & Management:**\n"]
            for d in departments:
                intake = d.get('intake_btech') or d.get('intake_pg', 'N/A')
                lines.append(f"• **{d['name']} ({d['short_name']})** – HOD: {d.get('hod')} (Intake: {intake} seats)")
            return ("\n".join(lines), default_source, "2025-26")

        # 4. Courses and Programs
        if action in ["LOOKUP_COURSES", "LOOKUP_ALL_PROGRAMS"]:
            programs = self.college_data.get("programs", [])
            lines = ["**Degree Programs Offered at PRPCEM (Autonomous):**\n"]
            for p in programs:
                lines.append(f"### {p['degree']} ({p['level']})")
                lines.append(f"• **Duration:** {p['duration']}")
                lines.append(f"• **Total Intake:** {p['total_intake']} seats")
                lines.append(f"• **Admission via:** {p['admission_exam']}")
                lines.append("• **Specializations / Branches:**")
                for b in p.get("branches", []):
                    lines.append(f"   - {b}")
                lines.append("")
            return ("\n".join(lines), default_source, "2025-26")

        if action == "LOOKUP_PROGRAM_DETAIL":
            prog_id = action_data.get("program") or entities.get("program")
            for p in self.college_data.get("programs", []):
                if prog_id.lower() in p["degree"].lower():
                    lines = [
                        f"### {p['degree']} ({p['level']})\n",
                        f"• **Duration:** {p['duration']}",
                        f"• **Total Seat Intake:** {p['total_intake']} seats",
                        f"• **Admission Route:** {p['admission_exam']}",
                        "• **Available Branches:**"
                    ]
                    for b in p.get("branches", []):
                        lines.append(f"   - {b}")
                    src = [{
                        "title": p.get("source_title", "PRPCEM Programs"),
                        "url": p.get("source_url", "https://prpotepatilengg.ac.in/")
                    }]
                    return ("\n".join(lines), src, p.get("academic_year", "2025-26"))

        # 5. Admissions, Eligibility, Documents
        if action == "LOOKUP_ADMISSION_PROCESS":
            adm = self.college_data.get("admissions", {})
            resp = (
                f"### Admission Process at PRPCEM (DTE Code: {adm.get('dte_code', '1107')})\n\n"
                f"{adm.get('admission_process')}\n\n"
                f"**Key Admission Requirements:**\n"
                f"• **B.Tech:** Centralized CAP rounds based on MHT-CET or JEE Main Paper-I score.\n"
                f"• **Direct Second Year (DSE):** Based on Engineering Diploma or B.Sc. merit.\n"
                f"• **MBA / MCA:** Through MAH-MBA-CET / MAH-MCA-CET centralized rounds.\n"
                f"• **M.Tech:** Based on GATE score / Non-GATE CAP round merit.\n\n"
                f"For admission inquiries, you can contact the admission cell: **+91 9371132222 / 9371142222**."
            )
            src = [{
                "title": adm.get("source_title", "PRPCEM Admissions"),
                "url": adm.get("source_url", "https://prpotepatilengg.ac.in/admission")
            }]
            return (resp, src, adm.get("academic_year", "2025-26"))

        if action == "LOOKUP_ELIGIBILITY":
            adm = self.college_data.get("admissions", {})
            resp = (
                "### Eligibility Criteria for Admission at PRPCEM:\n\n"
                f"**1. First Year B.Tech Eligibility:**\n{adm.get('btech_eligibility')}\n\n"
                f"**2. Direct Second Year (Lateral Entry) Eligibility:**\n{adm.get('direct_second_year_eligibility')}\n\n"
                f"**3. Postgraduate (M.Tech) Eligibility:**\n{adm.get('mtech_eligibility')}\n\n"
                f"**4. MBA Eligibility:**\n{adm.get('mba_eligibility')}\n\n"
                f"**5. MCA Eligibility:**\n{adm.get('mca_eligibility')}"
            )
            src = [{
                "title": adm.get("source_title", "PRPCEM Admissions & Eligibility"),
                "url": adm.get("source_url", "https://prpotepatilengg.ac.in/admission")
            }]
            return (resp, src, adm.get("academic_year", "2025-26"))

        if action == "LOOKUP_DOCUMENTS":
            adm = self.college_data.get("admissions", {})
            docs = adm.get("required_documents", [])
            lines = ["### Required Documents for Admission at PRPCEM:\n"]
            for i, doc in enumerate(docs, 1):
                lines.append(f"{i}. {doc}")
            lines.append("\n*(Note: Carry original documents along with 3 sets of self-attested photocopies during CAP reporting.)*")
            src = [{
                "title": adm.get("source_title", "PRPCEM Admission Document Checklist"),
                "url": adm.get("source_url", "https://prpotepatilengg.ac.in/admission")
            }]
            return ("\n".join(lines), src, adm.get("academic_year", "2025-26"))

        # 6. Fees, Scholarships, Intake
        if action == "LOOKUP_FEES":
            fee_info = self.college_data.get("fees", {})
            resp = (
                f"### PRPCEM Fee Structure (Academic Year 2025-26)\n\n"
                f"{fee_info.get('fee_structure_overview')}\n\n"
                f"• **Interim B.Tech Annual Tuition & Development Fee:** {fee_info.get('btech_interim_tuition_fee')}\n\n"
                f"**Fee Concessions through Government Scholarships:**\n"
                f"• **SC / ST Candidates:** 100% Tuition & Development Fee waiver via MahaDBT.\n"
                f"• **OBC / EBC Candidates:** 50% Tuition Fee waiver.\n"
                f"• **VJ / NT / SBC Candidates:** 100% Tuition Fee waiver as per state norms.\n"
                f"• **TFWS (Tuition Fee Waiver Scheme):** 100% Tuition Fee waiver for allotted candidates."
            )
            src = [{
                "title": fee_info.get("source_title", "PRPCEM Fee Structure"),
                "url": fee_info.get("source_url", "https://prpotepatilengg.ac.in/fees-structure-2022-2023")
            }]
            return (resp, src, fee_info.get("academic_year", "2025-26"))

        if action == "LOOKUP_SCHOLARSHIPS":
            fee_info = self.college_data.get("fees", {})
            scholarships = fee_info.get("scholarships", [])
            lines = ["### Scholarships and Financial Aid Schemes available at PRPCEM:\n"]
            for s in scholarships:
                lines.append(f"• **{s}**")
            lines.append("\nStudents can apply online through the Government of Maharashtra MahaDBT Portal (https://mahadbt.maharashtra.gov.in/).")
            src = [{
                "title": fee_info.get("source_title", "PRPCEM Scholarships"),
                "url": fee_info.get("source_url", "https://prpotepatilengg.ac.in/fees-structure-2022-2023")
            }]
            return ("\n".join(lines), src, fee_info.get("academic_year", "2025-26"))

        if action == "LOOKUP_INTAKE_DEPT":
            dept_id = action_data.get("department") or entities.get("department")
            for d in self.college_data.get("departments", []):
                if d["id"] == dept_id:
                    resp = f"The approved seat intake for **{d['name']} ({d['short_name']})** is **{d.get('intake_btech', d.get('intake_pg', 'N/A'))} seats** per academic year."
                    src = [{"title": d.get("source_title", "PRPCEM Department"), "url": d.get("source_url")}]
                    return (resp, src, "2025-26")

        if action == "LOOKUP_INTAKE_ALL":
            departments = self.college_data.get("departments", [])
            lines = ["### Seat Intake Capacity at PRPCEM:\n", "**Undergraduate (B.Tech) Programs:**"]
            total_ug = 0
            for d in departments:
                if d.get("intake_btech") and d["id"] != "fy":
                    lines.append(f"• {d['name']}: **{d['intake_btech']} seats**")
                    total_ug += d['intake_btech']
            lines.append(f"\n**Total B.Tech First Year Intake:** **{total_ug} seats**\n")
            lines.append("**Postgraduate (PG) Programs:**")
            for d in departments:
                if d.get("intake_pg"):
                    lines.append(f"• {d['name']}: **{d['intake_pg']} seats**")
                elif d.get("intake_mtech"):
                    lines.append(f"• M.Tech in {d['name']}: **{d['intake_mtech']} seats**")
            return ("\n".join(lines), default_source, "2025-26")

        # 7. Facilities (Library, Hostel, Labs, etc.)
        if action == "LOOKUP_LIBRARY":
            fac = self.kg.get_facility_info("Library")
            resp = (
                f"### PRPCEM Central Library Facility\n\n"
                f"{fac.get('description', 'Equipped with 35,000+ volumes, DELNET, and reading rooms.')}\n\n"
                f"• **Timings:** Open Monday to Saturday from 8:30 AM to 8:00 PM.\n"
                f"• **Digital Access:** Subscribed to IEEE Xplore, DELNET, and National Digital Library (NDL)."
            )
            src = [{"title": "PRPCEM Central Library", "url": "https://prpotepatilengg.ac.in/"}]
            return (resp, src, "2025-26")

        if action == "LOOKUP_HOSTEL":
            fac = self.kg.get_facility_info("Hostel")
            resp = (
                f"### PRPCEM Campus Hostel Facility\n\n"
                f"{fac.get('description', 'Separate residential hostels for Boys and Girls.')}\n\n"
                f"• **Amenities:** Wi-Fi internet, 24/7 power backup, CCTV surveillance, solar water heaters.\n"
                f"• **Mess:** Hygienic dining facility serving breakfast, lunch, and dinner.\n"
                f"• **Warden & Medical:** Resident wardens and emergency medical care on campus."
            )
            src = [{"title": "PRPCEM Hostels", "url": "https://prpotepatilengg.ac.in/"}]
            return (resp, src, "2025-26")

        if action == "LOOKUP_FACILITIES":
            facilities = self.college_data.get("facilities", [])
            lines = ["### Campus Facilities & Student Infrastructure at PRPCEM:\n"]
            for f in facilities:
                lines.append(f"• **{f['name']}:** {f['description']}\n")
            return ("\n".join(lines), default_source, "2025-26")

        if action == "LOOKUP_LABORATORIES":
            departments = self.college_data.get("departments", [])
            lines = ["### Department Laboratories & Computing Centers at PRPCEM:\n"]
            for d in departments:
                if d.get("laboratories"):
                    labs = ", ".join(d["laboratories"])
                    lines.append(f"• **{d['name']} ({d['short_name']}):**\n  {labs}\n")
            return ("\n".join(lines), default_source, "2025-26")

        # 8. Academics, Calendar, Syllabus, Examination, Notices
        if action == "LOOKUP_ACADEMIC_CALENDAR":
            acad = self.college_data.get("academic", {})
            resp = (
                "### PRPCEM Academic Calendar (Autonomous 2025-26 / 2026-27)\n\n"
                "The academic calendar is issued by the **Office of Dean (Academics)** and outlines:\n"
                "• Commencement of classes for Odd & Even Semesters\n"
                "• Continuous Internal Evaluation (CIE) and Mid-Term Tests\n"
                "• Submission and Practical Examination dates\n"
                "• End Semester Examination (ESE) schedules\n\n"
                "You can access and view the official teaching schedules on the Academic Portal."
            )
            src = [{
                "title": "PRPCEM Academic Calendars Portal",
                "url": "https://academics.prpotepatilengg.ac.in/academic-calendars"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_SYLLABUS":
            acad = self.college_data.get("academic", {})
            schemes = acad.get("schemes_and_syllabi", [])
            lines = [
                "### Autonomous Schemes and Syllabus (Academic Years 2025-26 / 2026-27):\n",
                "Course curriculum, credit structure, and detailed course syllabi for autonomous B.Tech and M.Tech programs are available on the Dean Academics portal:\n"
            ]
            for s in schemes:
                lines.append(f"• **{s['branch']}** (Academic Year {s['year']}): [View Scheme & Syllabus]({s['url']})")
            src = [{
                "title": "PRPCEM Dean Academics Schemes & Syllabus",
                "url": "https://academics.prpotepatilengg.ac.in/"
            }]
            return ("\n".join(lines), src, "2026-27")

        if action == "LOOKUP_EXAMINATION":
            acad = self.college_data.get("academic", {})
            exam_portal = acad.get("examination_portal", {})
            resp = (
                f"### Autonomous Examinations at PRPCEM\n\n"
                f"• **Grading System:** Autonomous continuous assessment + End-Semester Examinations (ESE) under SGBAU autonomy ordinance.\n"
                f"• **Online Examination Portal:** {exam_portal.get('name')}\n"
                f"• **Portal URL:** {exam_portal.get('url')}\n"
                f"• **Purpose:** Examination registration, backlog forms submission, timetable display, and hall tickets download."
            )
            src = [
                {"title": "PRPCEM Examination Forms Portal", "url": "https://prpcem.dotcominfotech.in/"},
                {"title": "Dean Academics Official Website", "url": "https://academics.prpotepatilengg.ac.in/"}
            ]
            return (resp, src, "2025-26")

        if action == "LOOKUP_NOTICES":
            notices = self.college_data.get("notices", [])
            lines = ["### Latest Official Notices from Dean (Academics) & Principal Office:\n"]
            sources = []
            for n in notices:
                lines.append(f"• **{n['title']}** (Academic Year {n.get('academic_year', '2025-26')})")
                lines.append(f"  {n['summary']}\n")
                sources.append({"title": n['title'], "url": n['url']})
            return ("\n".join(lines), sources, "2025-26")

        # 9. Overview, History, Vision/Mission, Leadership
        if action == "LOOKUP_COLLEGE_OVERVIEW":
            resp = (
                f"### About {college.get('name', 'PRPCEM')}\n\n"
                f"• **Established:** {college.get('established_year', 2009)} under the aegis of {college.get('trust')}.\n"
                f"• **Founder & Chairman:** {college.get('founder_chairman')}\n"
                f"• **Principal:** {college.get('principal')}\n"
                f"• **Dean Academics:** {college.get('dean_academics')}\n"
                f"• **Status:** {college.get('autonomy_status')}\n"
                f"• **Accreditation:** {college.get('accreditation')}\n"
                f"• **Affiliation & Approvals:** {college.get('affiliation')}; {college.get('approvals')}\n"
                f"• **DTE Code:** {college.get('dte_code')}\n"
                f"• **Location:** {college.get('location')}"
            )
            return (resp, default_source, college.get("academic_year", "2025-26"))

        if action == "LOOKUP_HISTORY":
            resp = (
                f"### History & Establishment of PRPCEM\n\n"
                f"P. R. Pote Patil College of Engineering & Management was established in **{college.get('established_year', 2009)}** "
                f"in Amravati by {college.get('founder_chairman')}.\n\n"
                f"Founded under the P. R. Pote (Patil) Education & Welfare Trust, the institute was created to deliver world-class technical education in the Vidarbha region. "
                f"Over the years, the institution has earned NAAC 'A' Grade accreditation (CGPA 3.07), autonomous status from UGC and Sant Gadge Baba Amravati University, "
                f"and expanded into a multi-disciplinary technical campus offering 7 B.Tech specializations, 4 M.Tech programs, MBA, and MCA."
            )
            return (resp, default_source, "2025-26")

        if action == "LOOKUP_VISION_MISSION":
            resp = (
                f"### Vision, Mission & Quality Policy of PRPCEM\n\n"
                f"**Vision:**\n{college.get('vision')}\n\n"
                f"**Mission:**\n{college.get('mission')}\n\n"
                f"**Quality Policy:**\n{college.get('quality_policy')}"
            )
            return (resp, default_source, "2025-26")

        # 10. Contact, Location, Autonomy, Accreditation, Placement
        if action == "LOOKUP_CONTACT":
            contact = self.college_data.get("contact", {})
            phones = ", ".join(contact.get("phone_numbers", []))
            emails = contact.get("emails", {})
            resp = (
                f"### Contact Information – PRPCEM Amravati\n\n"
                f"• **Address:** {contact.get('address')}\n"
                f"• **Helpline & Phone Numbers:** {phones}\n"
                f"• **Admission Inquiries:** {contact.get('admission_helpline')}\n"
                f"• **Principal Email:** {emails.get('principal')}\n"
                f"• **Dean Academics Email:** {emails.get('dean_academics')}\n"
                f"• **Working Timings:** {contact.get('timings')}\n"
                f"• **Official Portals:** {', '.join(contact.get('official_websites', []))}"
            )
            src = [{
                "title": contact.get("source_title", "PRPCEM Contact Directory"),
                "url": contact.get("source_url", "https://prpotepatilengg.ac.in/contact-us")
            }]
            return (resp, src, contact.get("academic_year", "2025-26"))

        if action == "LOOKUP_LOCATION":
            contact = self.college_data.get("contact", {})
            resp = (
                f"### Campus Location & Directions\n\n"
                f"**Address:**\n{contact.get('address')}\n\n"
                f"**How to reach PRPCEM:**\n"
                f"• The campus is situated at Pote Estate on **Kathora Road**, Amravati.\n"
                f"• Approximately 6 km from Amravati Railway Station and Central Bus Stand.\n"
                f"• Easily accessible by city buses, auto-rickshaws, and college bus transport."
            )
            src = [{
                "title": "PRPCEM Location & Campus Map",
                "url": "https://prpotepatilengg.ac.in/contact-us"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_AUTONOMY":
            resp = (
                f"### Autonomous Status & Governance\n\n"
                f"• **Autonomy:** P. R. Pote Patil College of Engineering & Management is an **Autonomous Institution** affiliated to Sant Gadge Baba Amravati University (SGBAU).\n"
                f"• **Curriculum Design:** The college designs its own industry-oriented autonomous syllabus, credit framework, and academic rules through Board of Studies (BOS) and Academic Council.\n"
                f"• **Degrees Conferred:** Degrees are awarded by Sant Gadge Baba Amravati University (SGBAU), Amravati.\n"
                f"• **Ordinance:** Governed by official autonomous academic ordinances and continuous assessment norms."
            )
            src = [{
                "title": "PRPCEM Autonomous Ordinance",
                "url": "https://academics.prpotepatilengg.ac.in/PRPCEM_Ordinance_23-24_DraftCopy.pdf"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_ACCREDITATION":
            resp = (
                f"### Accreditations, Approvals & Recognitions\n\n"
                f"• **NAAC Accreditation:** Accredited by NAAC with **Grade 'A'** (CGPA 3.07).\n"
                f"• **AICTE Approval:** Approved by the All India Council for Technical Education (AICTE), New Delhi.\n"
                f"• **Government Recognition:** Recognized by the Directorate of Technical Education (DTE), Govt. of Maharashtra (**DTE Code: 1107**).\n"
                f"• **University Affiliation:** Permanently affiliated to Sant Gadge Baba Amravati University (SGBAU).\n"
                f"• **Quality Certification:** ISO 9001:2015 certified institution."
            )
            return (resp, default_source, "2025-26")

        if action == "LOOKUP_PLACEMENT":
            resp = (
                "### Training & Placement Cell (T&P Cell)\n\n"
                "The Training and Placement Cell at PRPCEM actively conducts campus recruitment drives, skill bootcamps, and industrial internships.\n\n"
                "• **Key Campus Recruiters:** TCS, Infosys, Tech Mahindra, Cognizant, Wipro, Capgemini, L&T Infotech, Hexaware, Persistent Systems, and Symbiosis.\n"
                "• **Placement Preparation:** Regular coding classes in Python/Java/C++, aptitude training, mock interviews, and group discussion sessions.\n"
                "• **Industry Collaborations:** Active MOUs with top IT and core engineering companies for student internships."
            )
            src = [{
                "title": "PRPCEM Campus Placement Cell",
                "url": "https://prpotepatilengg.ac.in/campus-selection"
            }]
            return (resp, src, "2025-26")

        if action == "LOOKUP_FACULTY":
            departments = self.college_data.get("departments", [])
            lines = [
                "### Faculty & Academic Leadership at PRPCEM\n",
                f"• **Principal:** {college.get('principal')}",
                f"• **Dean (Academics):** {college.get('dean_academics')}\n",
                "**Department Heads & Professors:**"
            ]
            for d in departments:
                lines.append(f"• **{d['name']}:** {d.get('hod')}")
            return ("\n".join(lines), default_source, "2025-26")

        # Default Fallback
        return (
            f"{FALLBACK_MESSAGE}\n\n{FALLBACK_SUGGESTIONS}",
            default_source,
            "2025-26"
        )

# Global singleton instance
_response_generator_instance: Optional[ResponseGenerator] = None

def get_response_generator() -> ResponseGenerator:
    global _response_generator_instance
    if _response_generator_instance is None:
        _response_generator_instance = ResponseGenerator()
    return _response_generator_instance
