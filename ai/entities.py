"""
POTENTIAL AI - Named Entity Recognition Module
Extracts domain-specific entities (Departments, Programs, Academic Years, Info Types)
from user natural language queries using official PRPCEM institutional terminology.
"""

import re
from typing import Dict, Any, Optional, List

# Official PRPCEM Departments Mapping
DEPARTMENT_PATTERNS = [
    {
        "id": "cse_aiml",
        "name": "Computer Science and Engineering (Artificial Intelligence & Machine Learning)",
        "patterns": [
            r"\b(cse[\s\-_]*ai[\s\-_]*ml|cse[\s\-_]*aiml|ai[\s\-_]*ml|aiml|artificial\s+intelligence\s+(?:and|&)\s+machine\s+learning)\b"
        ]
    },
    {
        "id": "aids",
        "name": "Artificial Intelligence and Data Science",
        "patterns": [
            r"\b(ai[\s\-_]*ds|aids|ai\s+and\s+ds|artificial\s+intelligence\s+(?:and|&)\s+data\s+science|data\s+science)\b"
        ]
    },
    {
        "id": "cse",
        "name": "Computer Science and Engineering",
        "patterns": [
            r"\b(computer\s+science(?:\s+and\s+engineering)?|computer\s+engineering|cse|cs\s+dept|comp\s+sci|computer\s+branch)\b"
        ]
    },
    {
        "id": "extc",
        "name": "Electronics and Telecommunication Engineering",
        "patterns": [
            r"\b(electronics\s+(?:and|&)\s+telecommunication(?:\s+engineering)?|electronics\s+and\s+telecom|extc|e&tc|entc)\b"
        ]
    },
    {
        "id": "first_year",
        "name": "First Year Applied Sciences and Humanities",
        "patterns": [
            r"\b(first\s+year|applied\s+sciences|applied\s+physics|applied\s+chemistry|applied\s+math|humanities|fe\s+dept|first\s+year\s+engg)\b"
        ]
    },
    {
        "id": "mba",
        "name": "Master of Business Administration (MBA)",
        "patterns": [
            r"\b(mba|management\s+studies|master\s+of\s+business\s+administration|business\s+administration)\b"
        ]
    },
    {
        "id": "mca",
        "name": "Master of Computer Applications (MCA)",
        "patterns": [
            r"\b(mca|master\s+of\s+computer\s+applications|computer\s+applications)\b"
        ]
    },
    {
        "id": "ce",
        "name": "Civil Engineering",
        "patterns": [
            r"\b(civil\s+engineering|civil\s+engg|civil\s+dept|civil\s+branch|civil|ce\s+dept|ce\s+branch|ce\s+department)\b"
        ]
    },
    {
        "id": "me",
        "name": "Mechanical Engineering",
        "patterns": [
            r"\b(mechanical\s+engineering|mechanical\s+engg|mech\s+dept|mech\s+branch|mechanical|mech|me\s+dept|me\s+branch|me\s+department)\b"
        ]
    },
    {
        "id": "ee",
        "name": "Electrical Engineering",
        "patterns": [
            r"\b(electrical\s+engineering|electrical\s+engg|electrical\s+dept|electrical\s+branch|electrical|ee\s+dept|ee\s+branch|ee\s+department)\b"
        ]
    }
]

# Official Programs Mapping
PROGRAM_PATTERNS = [
    {
        "id": "mca",
        "name": "Master of Computer Applications (MCA)",
        "patterns": [r"\b(mca|master\s+of\s+computer\s+applications)\b"]
    },
    {
        "id": "mba",
        "name": "Master of Business Administration (MBA)",
        "patterns": [r"\b(mba|master\s+of\s+business\s+administration)\b"]
    },
    {
        "id": "mtech",
        "name": "Master of Technology (M.Tech / M.E.)",
        "patterns": [r"\b(m\.?\s*tech|m\.?\s*e(?:\s+in|\s+degree|\s+engg)?|postgraduate|pg|master(?:\s+of\s+technology)?)\b"]
    },
    {
        "id": "btech",
        "name": "Bachelor of Technology (B.Tech / B.E.)",
        "patterns": [r"\b(b\.?\s*tech|b\.?\s*e(?:\s+in|\s+degree|\s+engg)?|undergraduate|ug|bachelor(?:\s+of\s+technology)?)\b"]
    }
]

# Academic Year Recognition
YEAR_PATTERNS = [
    (r"\b2026[\-_/]?27\b", "2026-27"),
    (r"\b2025[\-_/]?26\b", "2025-26"),
    (r"\b2024[\-_/]?25\b", "2024-25"),
    (r"\bcurrent\s+year\b", "2025-26"),
    (r"\bnext\s+year\b", "2026-27")
]

# Information Type Recognition
INFO_TYPE_PATTERNS = [
    (r"\b(principal|head\s+of\s+college|director\s+or\s+principal|dr\s+jawandhiya|jawandhiya)\b", "principal"),
    (r"\b(chairman|founder|founder\s+chairman|vice\s+chairman|president\s+of\s+the\s+trust|pravinkumar|pravin\s+pote|shreyash\s+pote|trustee)\b", "chairman"),
    (r"\b(dean\s+of\s+academics|dean\s+academics|academic\s+dean|dr\s+kute|dean)\b", "dean"),
    (r"\b(leadership|management\s+of\s+prpcem|board\s+of\s+trustees|governing\s+body|key\s+administrators|college\s+leaders)\b", "leadership"),
    (r"\b(hod|head\s+of\s+department|department\s+head|who\s+heads)\b", "hod"),
    (r"\b(fee|fees|cost|tuition|payment|fra)\b", "fees"),
    (r"\b(admission|admissions|apply|cap\s+rounds?|dte|seat\s+allotment)\b", "admission"),
    (r"\b(eligibility|criteria|qualification|requirements?|cut[\-_]?off)\b", "eligibility"),
    (r"\b(document|documents|certificate|certificates|checklist)\b", "documents"),
    (r"\b(scholarship|scholarships|ebc|mahadbt|tfws|concession)\b", "scholarship"),
    (r"\b(intake|seats|capacity|intake\s+capacity)\b", "intake"),
    (r"\b(syllabus|curriculum|scheme|course\s+structure)\b", "syllabus"),
    (r"\b(calendar|academic\s+calendar|schedule|semester\s+dates?)\b", "academic_calendar"),
    (r"\b(library|books|journals|delnet|ndl|reading\s+hall)\b", "library"),
    (r"\b(hostel|accommodation|stay|rooms?|mess)\b", "hostel"),
    (r"\b(facility|facilities|campus|infrastructure|sports|gym)\b", "facilities"),
    (r"\b(lab|labs|laboratory|laboratories|computing\s+center)\b", "laboratories"),
    (r"\b(faculty|professors?|teachers?|staff)\b", "faculty"),
    (r"\b(placement|placements|jobs|recruiters|packages?|t&p)\b", "placement"),
    (r"\b(exam|exams|examination|results?|hall\s+tickets?)\b", "examination"),
    (r"\b(notice|notices|announcements?|circulars?)\b", "notices"),
    (r"\b(contact|phone|email|helpline|address|location|reach)\b", "contact")
]

def extract_entities(query_text: str) -> Dict[str, Any]:
    """
    Extracts structured entities from input query.
    Returns:
        {
            "department": str or None,
            "department_name": str or None,
            "program": str or None,
            "program_name": str or None,
            "academic_year": str or None,
            "info_type": str or None,
            "matched_entities": list
        }
    """
    if not query_text:
        return {
            "department": None,
            "department_name": None,
            "program": None,
            "program_name": None,
            "academic_year": None,
            "info_type": None,
            "matched_entities": []
        }

    text_lower = query_text.lower().strip()
    matched_entities: List[str] = []

    # 1. Match Department
    matched_dept_id = None
    matched_dept_name = None
    for dept in DEPARTMENT_PATTERNS:
        for pat in dept["patterns"]:
            if re.search(pat, text_lower, re.IGNORECASE):
                matched_dept_id = dept["id"]
                matched_dept_name = dept["name"]
                matched_entities.append(f"Department: {dept['name']}")
                break
        if matched_dept_id:
            break

    # 2. Match Program
    matched_prog_id = None
    matched_prog_name = None
    for prog in PROGRAM_PATTERNS:
        for pat in prog["patterns"]:
            if re.search(pat, text_lower, re.IGNORECASE):
                matched_prog_id = prog["id"]
                matched_prog_name = prog["name"]
                matched_entities.append(f"Program: {prog['name']}")
                break
        if matched_prog_id:
            break

    # 3. Match Academic Year
    matched_year = None
    for pat, yr in YEAR_PATTERNS:
        if re.search(pat, text_lower, re.IGNORECASE):
            matched_year = yr
            matched_entities.append(f"Academic Year: {yr}")
            break

    # 4. Match Info Type
    matched_info_type = None
    for pat, itype in INFO_TYPE_PATTERNS:
        if re.search(pat, text_lower, re.IGNORECASE):
            matched_info_type = itype
            matched_entities.append(f"Info Type: {itype}")
            break

    return {
        "department": matched_dept_id,
        "department_name": matched_dept_name,
        "program": matched_prog_id,
        "program_name": matched_prog_name,
        "academic_year": matched_year,
        "info_type": matched_info_type,
        "matched_entities": matched_entities
    }
