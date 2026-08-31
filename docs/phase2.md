# POTENTIAL AI - Phase 2 to Final Deployment Engineering Report

**Institution:** P. R. Pote Patil College of Engineering & Management, Amravati (PRPCEM)  
**Project:** Potential AI - Intelligent College Assistant Chatbot  
**Documentation:** Phases 2 through 50 Implementation Traceability  

---

## 1. Executive Summary
This document provides complete technical specifications for the implementation of Phases 2 through 50 of **POTENTIAL AI**. The project demonstrates a privacy-first, zero-cost, and explainable intelligent college chatbot assistant and algorithm laboratory built strictly upon syllabus-compliant artificial intelligence technologies without any external or paid LLM APIs.

---

## 2. Engineering Architecture

```
                                  USER
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ Frontend Web UI    │
                         │ (HTML5/CSS3/JS)    │
                         └─────────┬──────────┘
                                   │  HTTP POST /api/chat
                                   ▼
                         ┌────────────────────┐
                         │ Flask Web Server   │
                         │ (app.py, WSGI)     │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Input Validation   │
                         │ & Sanitization     │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ NLP Preprocessing  │
                         │ (ai/preprocess.py) │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ TF-IDF Vectorizer  │
                         │ (models/vector.pkl)│
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ LogisticRegression │ ──► Predicted Intent & Softmax Confidence
                         │ (models/model.pkl) │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Entity Extractor   │ ──► Departments, Programs, Academic Years
                         │ (ai/entities.py)   │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Experta Engine     │ ──► Salience Rules & Forward-Chaining
                         │ (ai/rules.py)      │
                         └─────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
         ┌────────────────────┐        ┌────────────────────┐
         │ Knowledge Base     │        │ NetworkX Graph     │
         │ (ai/knowledge.py)  │        │ (knowledge_graph)  │
         └──────────┬─────────┘        └──────────┬─────────┘
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Response Generator │ ──► Verified Answer + Academic Year
                         │ (ai/response.py)   │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Source Attribution │ ──► Direct Official PRPCEM Source URLs
                         │ (data/sources.json)│
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ SQLite Logger      │ ──► Logged to potential_ai.db
                         │ (database.py)      │
                         └─────────┬──────────┘
                                   │
                                   ▼
                                  USER
```

---

## 3. Detailed Component Specifications

### 3.1 Knowledge Base & Schema (`data/processed/college_data.json`)
The canonical structured knowledge base stores official records categorized into:
* **College:** Name, trust, establishment year (2009), autonomy status, NAAC 'A' grade (CGPA 3.07), DTE Code (1107), SGBAU affiliation, leadership (Principal Dr. D. T. Ingole, Dean Dr. Mohammad Zuhair).
* **Departments (10):** CSE, CSE (AIML), AI&DS, Civil, Mechanical, Electrical, EXTC, First Year, MBA, MCA.
* **Programs (4):** B.Tech, M.Tech, MBA, MCA with durations, seat intakes, and admission exams.
* **Admissions & Documents:** Centralized CAP admission process, eligibility criteria, and 14-item required document checklist.
* **Fees & Scholarships:** FRA sanctioned tuition fees, MahaDBT, EBC, SC/ST, and TFWS schemes.
* **Facilities:** Central Library (35,000+ volumes, DELNET, NDL), Hostels, Sports, Transport, T&P Cell.

### 3.2 Machine Learning & Intent Classification (`ai/classifier.py`)
* **Dataset:** `data/intents.csv` (278+ labeled questions across 30 intents).
* **Vectorization:** `TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True)`.
* **Model:** `LogisticRegression(C=10.0, max_iter=1000, class_weight='balanced')`.
* **Metrics:** Accuracy: 71.43%, Precision: 73.96%, Recall: 71.43%, F1 Score: 70.84%.
* **Confidence Threshold:** `CONFIDENCE_THRESHOLD = 0.35`. Low-confidence queries without matching entities safely trigger fallback.

### 3.3 Named Entity Recognition (`ai/entities.py`)
Regex patterns with strict word boundaries extract:
* Departments (`cse`, `cse_aiml`, `aids`, `ce`, `me`, `ee`, `extc`, `first_year`, `mba`, `mca`).
* Degree programs (`btech`, `mtech`, `mba`, `mca`).
* Academic years (`2025-26`, `2026-27`).
* Information types (`hod`, `fees`, `admission`, `eligibility`, `documents`, `scholarship`, `intake`, `syllabus`, `calendar`, `library`, `hostel`, `facilities`, `laboratories`, `faculty`, `placement`, `examination`, `notices`, `contact`).

### 3.4 Experta Symbolic Rule Engine (`ai/rules.py`)
* Declares Facts: `UserQuery`, `QueryIntent`, `ExtractedEntity`, `CollegeAction`.
* Forward chaining inference with salience priorities:
  * Salience 10: Specific entity rules (`rule_hod_specific_department`, `rule_department_specific`, `rule_program_specific`, `rule_intake_dept`).
  * Salience 5: General category rules (`rule_hod_all_departments`, `rule_department_list`, `rule_program_all`).
* Python 3.10+ / 3.13 compatibility enabled via `collections.abc` shims.

### 3.5 NetworkX Knowledge Graph (`ai/knowledge_graph.py`)
* Builds a directed graph (`nx.DiGraph`) containing 37 nodes and 46 relational edges (`HAS_DEPARTMENT`, `HEADED_BY`, `OFFERS_PROGRAM`, `PROVIDES_FACILITY`).
* Enables graph traversal methods: `get_department_info()`, `get_hod()`, `get_all_hods()`, `get_facility_info()`, `get_related_entities()`.

### 3.6 AI Algorithm Laboratory (`algorithms/`)
Full implementations of:
1. `bfs.py`: Breadth-First Search ($O(b^d)$ time & space).
2. `dfs.py`: Depth-First Search ($O(b^m)$ time, $O(bm)$ space).
3. `ucs.py`: Uniform Cost Search ($O(b^{1+\lfloor C^*/\epsilon\rfloor})$).
4. `astar.py`: A* Search ($f(n) = g(n) + h(n)$).
5. `greedy.py`: Greedy Best-First Search ($f(n) = h(n)$).
6. `hill_climbing.py`: Steepest-ascent optimization.
7. `genetic.py`: Binary chromosome population evolutionary optimization.
8. `minimax.py`: Game tree search for Tic-Tac-Toe.
9. `alpha_beta.py`: Game tree search with $\alpha \ge \beta$ branch pruning.
10. `water_jug.py`: Water Jug problem BFS state-space search solver.
11. `missionaries_cannibals.py`: River crossing BFS state-space search solver.

---

## 4. Verification & Testing
The project includes a 37-test automated Pytest suite covering all modules:
* `tests/test_preprocess.py` (3 tests)
* `tests/test_classifier.py` (2 tests)
* `tests/test_entities.py` (5 tests)
* `tests/test_knowledge.py` (6 tests)
* `tests/test_rules.py` (4 tests)
* `tests/test_knowledge_graph.py` (3 tests)
* `tests/test_chatbot.py` (2 tests)
* `tests/test_algorithms.py` (5 tests)
* `tests/test_web_routes.py` (7 tests)

**Result:** 37 passed in ~3.5s (100% pass rate).
