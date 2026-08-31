"""
NetworkX Knowledge Graph Module for Potential AI.
Constructs an interconnected semantic knowledge graph representing PRPCEM entities,
departments, leadership, programs, facilities, and academic resources.
"""

import os
import json
import networkx as nx
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "college_data.json")

class CollegeKnowledgeGraph:
    def __init__(self, data_path: str = DATA_PATH):
        self.data_path = data_path
        self.graph = nx.DiGraph()
        self.raw_data = {}
        self.build_graph()

    def build_graph(self):
        """Construct the NetworkX directed graph from structured JSON data."""
        if not os.path.exists(self.data_path):
            print(f"[KnowledgeGraph] Warning: Data file {self.data_path} not found.")
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)

        self.graph.clear()
        college = self.raw_data.get("college", {})
        root_id = "PRPCEM"
        self.graph.add_node(
            root_id,
            name=college.get("name", "P. R. Pote Patil College of Engineering & Management"),
            type="institution",
            established=college.get("established_year", 2009),
            dte_code=college.get("dte_code", "1107"),
            accreditation=college.get("accreditation", "NAAC 'A' Grade"),
            autonomy=college.get("autonomy_status", "Autonomous"),
            location=college.get("location", "Kathora Road, Amravati")
        )

        # 1. Leadership: Chairman, Vice-Chairman, Principal, Dean
        founder_name = college.get("founder_chairman", "Shri Pravinkumar R. Pote Patil")
        self.graph.add_node(founder_name, name=founder_name, type="leadership", role="Founder & Chairman")
        self.graph.add_edge(root_id, founder_name, relation="FOUNDED_BY", role="Founder & Chairman")

        vice_name = college.get("vice_chairman", "Shri Shreyash P. Pote")
        self.graph.add_node(vice_name, name=vice_name, type="leadership", role="Vice-Chairman")
        self.graph.add_edge(root_id, vice_name, relation="VICE_CHAIRMAN", role="Vice-Chairman")

        principal_name = college.get("principal", "Dr. P. M. Jawandhiya")
        self.graph.add_node(principal_name, name=principal_name, type="leadership", role="Principal")
        self.graph.add_edge(root_id, principal_name, relation="LED_BY", role="Principal")

        dean_name = college.get("dean_academics", "Dr. V. B. Kute")
        self.graph.add_node(dean_name, name=dean_name, type="leadership", role="Dean Academics")
        self.graph.add_edge(root_id, dean_name, relation="ACADEMIC_HEAD", role="Dean (Academics)")

        # 2. Departments and HODs
        for dept in self.raw_data.get("departments", []):
            dept_id = dept["id"]
            self.graph.add_node(
                dept_id,
                name=dept["name"],
                short_name=dept["short_name"],
                type="department",
                intake_btech=dept.get("intake_btech", 0),
                intake_mtech=dept.get("intake_mtech", 0),
                laboratories=dept.get("laboratories", []),
                source_url=dept.get("source_url", "")
            )
            self.graph.add_edge(root_id, dept_id, relation="HAS_DEPARTMENT")

            # HOD Node & Edge
            hod_name = dept.get("hod")
            if hod_name:
                self.graph.add_node(hod_name, name=hod_name, type="person", role="HOD", department=dept["name"])
                self.graph.add_edge(dept_id, hod_name, relation="HEADED_BY")
                self.graph.add_edge(hod_name, dept_id, relation="HEAD_OF")

        # 3. Programs Offered
        for prog in self.raw_data.get("programs", []):
            degree_name = prog["degree"]
            self.graph.add_node(
                degree_name,
                name=degree_name,
                type="program",
                level=prog.get("level", ""),
                duration=prog.get("duration", ""),
                total_intake=prog.get("total_intake", 0),
                admission_exam=prog.get("admission_exam", "")
            )
            self.graph.add_edge(root_id, degree_name, relation="OFFERS_PROGRAM")

        # 4. Facilities
        for fac in self.raw_data.get("facilities", []):
            fac_name = fac["name"]
            self.graph.add_node(
                fac_name,
                name=fac_name,
                type="facility",
                description=fac.get("description", ""),
                source_url=fac.get("source_url", "")
            )
            self.graph.add_edge(root_id, fac_name, relation="PROVIDES_FACILITY")

        # 5. Academic Resources
        self.graph.add_node(
            "Academic_Calendar",
            name="PRPCEM Academic Calendar",
            type="academic_resource",
            url=self.raw_data.get("academic", {}).get("source_url", "")
        )
        self.graph.add_edge(root_id, "Academic_Calendar", relation="HAS_ACADEMIC_RESOURCE")

        self.graph.add_node(
            "Examination_Portal",
            name="Online Examination Forms Portal",
            type="academic_resource",
            url="https://prpcem.dotcominfotech.in/"
        )
        self.graph.add_edge(root_id, "Examination_Portal", relation="EXAM_PORTAL")

        print(f"[KnowledgeGraph] Successfully built graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")

    def get_department_info(self, dept_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve department attributes and connected HOD from the graph."""
        if dept_id in self.graph:
            node_data = dict(self.graph.nodes[dept_id])
            hods = [target for _, target, data in self.graph.out_edges(dept_id, data=True) if data.get("relation") == "HEADED_BY"]
            node_data["hod"] = hods[0] if hods else "Not specified"
            return node_data
        return None

    def get_hod(self, dept_id: str) -> Optional[str]:
        """Find the HOD for a department via graph traversal."""
        if dept_id in self.graph:
            for _, target, data in self.graph.out_edges(dept_id, data=True):
                if data.get("relation") == "HEADED_BY":
                    return target
        return None

    def get_all_hods(self) -> List[Dict[str, str]]:
        """List all departments and their respective HODs via graph traversal."""
        results = []
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "department":
                hod = self.get_hod(node)
                results.append({
                    "department_id": node,
                    "department_name": data.get("name", node),
                    "hod": hod or "Not specified"
                })
        return results

    def get_facility_info(self, facility_name_substring: str) -> Optional[Dict[str, Any]]:
        """Search facility node in knowledge graph."""
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "facility" and facility_name_substring.lower() in node.lower():
                return dict(data)
        return None

    def get_related_entities(self, entity_id: str) -> List[Dict[str, Any]]:
        """Return all outbound neighbors and relationship types for a node."""
        if entity_id not in self.graph:
            return []
        related = []
        for _, neighbor, data in self.graph.out_edges(entity_id, data=True):
            related.append({
                "entity": neighbor,
                "relationship": data.get("relation", "CONNECTED_TO"),
                "details": dict(self.graph.nodes[neighbor])
            })
        return related

    def get_principal(self) -> Dict[str, Any]:
        """Retrieve Principal name and details from knowledge graph."""
        college = self.raw_data.get("college", {})
        return {
            "name": college.get("principal", "Dr. P. M. Jawandhiya"),
            "role": "Principal",
            "college": college.get("name", "PRPCEM, Amravati"),
            "source_url": college.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def get_chairman(self) -> Dict[str, Any]:
        """Retrieve Founder & Chairman and Vice-Chairman details from knowledge graph."""
        college = self.raw_data.get("college", {})
        return {
            "founder_chairman": college.get("founder_chairman", "Shri Pravinkumar R. Pote Patil"),
            "vice_chairman": college.get("vice_chairman", "Shri Shreyash P. Pote"),
            "trust": college.get("trust", "P. R. Pote (Patil) Education & Welfare Trust"),
            "source_url": college.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def get_dean(self) -> Dict[str, Any]:
        """Retrieve Dean (Academics) details from knowledge graph."""
        college = self.raw_data.get("college", {})
        return {
            "name": college.get("dean_academics", "Dr. V. B. Kute"),
            "role": "Dean (Academics)",
            "office": "Office of Dean (Academics), PRPCEM",
            "source_url": "https://academics.prpotepatilengg.ac.in/"
        }

    def get_leadership(self) -> Dict[str, Any]:
        """Retrieve complete key leadership team from knowledge graph."""
        college = self.raw_data.get("college", {})
        return {
            "founder_chairman": college.get("founder_chairman", "Shri Pravinkumar R. Pote Patil"),
            "vice_chairman": college.get("vice_chairman", "Shri Shreyash P. Pote"),
            "principal": college.get("principal", "Dr. P. M. Jawandhiya"),
            "dean_academics": college.get("dean_academics", "Dr. V. B. Kute"),
            "trust": college.get("trust", "P. R. Pote (Patil) Education & Welfare Trust"),
            "source_url": college.get("source_url", "https://prpotepatilengg.ac.in/about-college")
        }

    def find_path(self, start_node: str, end_node: str) -> List[str]:
        """Find shortest relationship path between two knowledge nodes."""
        try:
            return nx.shortest_path(self.graph, start_node, end_node)
        except Exception:
            return []

# Singleton instance
_kg_instance: Optional[CollegeKnowledgeGraph] = None

def get_knowledge_graph() -> CollegeKnowledgeGraph:
    global _kg_instance
    if _kg_instance is None:
        _kg_instance = CollegeKnowledgeGraph()
    return _kg_instance
