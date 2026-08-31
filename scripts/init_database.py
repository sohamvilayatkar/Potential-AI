"""
Database Initialization Script for Potential AI.
Creates the SQLite database and schema, and seeds realistic sample queries
to demonstrate the analytics dashboard and Matplotlib chart generation.
"""

import os
import sys
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database import init_db, log_query, get_db_connection

SAMPLE_SEED_DATA = [
    ("What courses are offered at PRPCEM?", "courses", 0.96, "success"),
    ("Who is the HOD of Computer Engineering?", "hod", 0.94, "success"),
    ("What is the admission process for B.Tech?", "admission", 0.91, "success"),
    ("What documents are required for CAP rounds?", "documents", 0.89, "success"),
    ("Tell me about the college fee structure and scholarships", "fees", 0.92, "success"),
    ("What is the seat intake for AIML branch?", "intake", 0.88, "success"),
    ("Where is the Central Library located?", "library", 0.87, "success"),
    ("Is hostel facility available on campus?", "hostel", 0.93, "success"),
    ("Show me the autonomous academic calendar", "academic_calendar", 0.90, "success"),
    ("Who is the principal of PRPCEM?", "college_information", 0.95, "success"),
    ("What is the NAAC accreditation grade?", "accreditation", 0.92, "success"),
    ("Tell me about campus placements and top recruiters", "placement", 0.91, "success"),
    ("What is the eligibility for Direct Second Year Engineering?", "eligibility", 0.89, "success"),
    ("How to contact the admission helpline?", "contact", 0.94, "success"),
    ("What are the college working hours?", "college_information", 0.86, "success"),
    ("What is quantum string theory in space?", "fallback", 0.22, "fallback"),
    ("Which companies visited for campus selection?", "placement", 0.93, "success"),
    ("Can I get EBC scholarship fee concession?", "scholarship", 0.90, "success"),
    ("Show me syllabus for Mechanical Engineering", "syllabus", 0.91, "success"),
    ("Where to fill online examination form?", "examination", 0.95, "success"),
    ("How many seats in Civil Engineering?", "intake", 0.88, "success"),
    ("What is the DTE code for PRPCEM?", "accreditation", 0.94, "success"),
    ("Tell me something unrelated to college", "fallback", 0.18, "fallback"),
    ("Who is the HOD of Electrical Engineering?", "hod", 0.93, "success")
]

def initialize_and_seed():
    print("Initializing SQLite database...")
    init_db()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM queries_log")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        print("Seeding sample conversational queries for analytics...")
        for msg, intent, conf, status in SAMPLE_SEED_DATA:
            log_query(msg, intent, conf, status)
        print(f"Successfully seeded {len(SAMPLE_SEED_DATA)} queries into database.")
    else:
        print(f"Database already contains {count} query logs.")

if __name__ == "__main__":
    initialize_and_seed()
