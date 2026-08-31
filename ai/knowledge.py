"""
POTENTIAL AI - Knowledge Retrieval Layer
Provides structured lookup, categorization, attribute search, and source attribution
from the authoritative canonical PRPCEM knowledge base (college_data.json).
"""

import os
import json
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "college_data.json")
SOURCES_PATH = os.path.join(BASE_DIR, "data", "sources.json")

class KnowledgeBase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KnowledgeBase, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        self.data: Dict[str, Any] = {}
        self.sources: List[Dict[str, Any]] = []

        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"[KnowledgeBase Error] Failed to load college_data.json: {e}")
                self.data = {}

        if os.path.exists(SOURCES_PATH):
            try:
                with open(SOURCES_PATH, "r", encoding="utf-8") as f:
                    self.sources = json.load(f)
            except Exception as e:
                print(f"[KnowledgeBase Error] Failed to load sources.json: {e}")
                self.sources = []

    def get_college_overview(self) -> Dict[str, Any]:
        """Returns institutional profile and leadership."""
        return self.data.get("college", {})

    def get_principal_info(self) -> Dict[str, Any]:
        """Returns Principal details."""
        col = self.get_college_overview()
        return {
            "name": col.get("principal", "Dr. P. M. Jawandhiya"),
            "role": "Principal",
            "college": col.get("name", "PRPCEM, Amravati"),
            "source_url": col.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def get_chairman_info(self) -> Dict[str, Any]:
        """Returns Founder & Chairman and Vice-Chairman details."""
        col = self.get_college_overview()
        return {
            "founder_chairman": col.get("founder_chairman", "Shri Pravinkumar R. Pote Patil"),
            "vice_chairman": col.get("vice_chairman", "Shri Shreyash P. Pote"),
            "trust": col.get("trust", "P. R. Pote (Patil) Education & Welfare Trust"),
            "source_url": col.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def get_dean_info(self) -> Dict[str, Any]:
        """Returns Dean (Academics) details."""
        col = self.get_college_overview()
        return {
            "name": col.get("dean_academics", "Dr. V. B. Kute"),
            "role": "Dean (Academics)",
            "office": "Office of Dean (Academics), PRPCEM",
            "source_url": "https://academics.prpotepatilengg.ac.in/"
        }

    def get_leadership_info(self) -> Dict[str, Any]:
        """Returns structured leadership team."""
        col = self.get_college_overview()
        return {
            "founder_chairman": col.get("founder_chairman", "Shri Pravinkumar R. Pote Patil"),
            "vice_chairman": col.get("vice_chairman", "Shri Shreyash P. Pote"),
            "principal": col.get("principal", "Dr. P. M. Jawandhiya"),
            "dean_academics": col.get("dean_academics", "Dr. V. B. Kute"),
            "trust": col.get("trust", "P. R. Pote (Patil) Education & Welfare Trust"),
            "source_url": col.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def get_departments(self) -> List[Dict[str, Any]]:
        """Returns all 10 academic departments with intake and laboratories."""
        return self.data.get("departments", [])

    def get_department(self, dept_id: str) -> Optional[Dict[str, Any]]:
        """Lookup single department by ID or short name."""
        dept_id_clean = (dept_id or "").lower().strip()
        for d in self.get_departments():
            if d.get("id", "").lower() == dept_id_clean or d.get("short_name", "").lower() == dept_id_clean:
                return d
        return None

    def get_programs(self) -> List[Dict[str, Any]]:
        """Returns all undergraduate and postgraduate degree programs."""
        return self.data.get("programs", [])

    def get_admission_info(self) -> Dict[str, Any]:
        """Returns CAP admission process, eligibility, and 14-item document checklist."""
        return self.data.get("admissions", {})

    def get_fee_info(self) -> Dict[str, Any]:
        """Returns FRA fee structure and government scholarships (MahaDBT, EBC, TFWS)."""
        return self.data.get("fees", {})

    def get_facilities(self) -> List[Dict[str, Any]]:
        """Returns all campus facilities (Library, Hostels, Sports, T&P)."""
        return self.data.get("facilities", [])

    def get_facility(self, facility_name: str) -> Optional[Dict[str, Any]]:
        """Lookup specific facility by keyword."""
        fac_clean = (facility_name or "").lower().strip()
        for f in self.get_facilities():
            if fac_clean in f.get("name", "").lower() or fac_clean in f.get("id", "").lower():
                return f
        return None

    def get_academic_info(self) -> Dict[str, Any]:
        """Returns Dean Academics office and autonomous ordinance regulations."""
        return self.data.get("academic", {})

    def get_notices(self) -> List[Dict[str, Any]]:
        """Returns latest academic notices from Dean Academics & Principal office."""
        return self.data.get("notices", [])

    def get_contact_info(self) -> Dict[str, Any]:
        """Returns campus address, helpline numbers, and official emails."""
        return self.data.get("contact", {})

    def get_sources(self) -> List[Dict[str, Any]]:
        """Returns official source registry."""
        if isinstance(self.sources, dict) and "sources" in self.sources:
            return self.sources["sources"]
        if isinstance(self.sources, list) and len(self.sources) > 0:
            return self.sources
        return self.data.get("sources", [])

    def get_by_category(self, category: str) -> Any:
        """Retrieves structured section by top-level category."""
        return self.data.get(category.lower().strip())

    def get_by_entity(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """Finds any matching department, program, or facility entity."""
        dept = self.get_department(entity_name)
        if dept:
            return {"type": "department", "data": dept}
        fac = self.get_facility(entity_name)
        if fac:
            return {"type": "facility", "data": fac}
        for prog in self.get_programs():
            if entity_name.lower() in prog.get("degree", "").lower() or entity_name.lower() in prog.get("id", "").lower():
                return {"type": "program", "data": prog}
        return None

    def get_by_academic_year(self, year: str) -> List[Dict[str, Any]]:
        """Finds items specifically tagged with an academic year (e.g. '2025-26')."""
        results = []
        target_yr = (year or "").strip()
        # Check admissions & fees
        admissions = self.get_admission_info()
        if admissions.get("academic_year") == target_yr:
            results.append({"category": "admissions", "data": admissions})
        fees = self.get_fee_info()
        if fees.get("academic_year") == target_yr:
            results.append({"category": "fees", "data": fees})
        for n in self.get_notices():
            if n.get("academic_year") == target_yr:
                results.append({"category": "notice", "data": n})
        return results

    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Performs structured keyword matching across all knowledge records."""
        query_tokens = query.lower().split()
        results = []

        # Search departments
        for d in self.get_departments():
            d_str = json.dumps(d).lower()
            if any(token in d_str for token in query_tokens):
                results.append({"category": "department", "item": d})

        # Search facilities
        for f in self.get_facilities():
            f_str = json.dumps(f).lower()
            if any(token in f_str for token in query_tokens):
                results.append({"category": "facility", "item": f})

        return results

def get_knowledge_base() -> KnowledgeBase:
    """Singleton getter for KnowledgeBase."""
    return KnowledgeBase()
