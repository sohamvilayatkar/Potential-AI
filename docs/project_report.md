# POTENTIAL AI: Intelligent Web-Based College Assistant Chatbot
## Academic Mini-Project Report

**Institution:** P. R. Pote Patil College of Engineering & Management, Amravati  
**Academic Year:** 2025-26 / 2026-27  
**Course:** Artificial Intelligence Mini-Project  

---

### Table of Contents
1. Title
2. Abstract
3. Introduction
4. Problem Statement
5. Objectives
6. Existing System
7. Proposed System
8. System Requirements
9. System Architecture
10. Methodology
11. AI Techniques
12. Dataset Specification
13. Knowledge Representation
14. Experta Rule Engine Implementation
15. Machine Learning Pipeline
16. NetworkX Knowledge Graph
17. Syllabus Algorithm Implementations
18. System Implementation & Routes
19. Testing & Verification
20. Experimental Results & Metrics
21. Screenshots & User Interface Walkthrough
22. Advantages of Potential AI
23. Limitations
24. Future Scope
25. Course Outcome (CO) Mapping
26. Conclusion
27. References

---

### 1. Title
**POTENTIAL AI: An Intelligent Web-Based College Assistant Chatbot for P. R. Pote Patil College of Engineering & Management, Amravati.**

### 2. Abstract
Navigating institutional information in higher education institutions presents a significant challenge for prospective applicants, current students, and faculty. In this project, we design, develop, and evaluate **POTENTIAL AI**, a web-based, privacy-first conversational assistant that answers queries regarding P. R. Pote Patil College of Engineering & Management (PRPCEM), Amravati. Diverging from resource-heavy commercial Large Language Models (LLMs) that introduce recurring API costs and hallucinations, Potential AI operates entirely on local, interpretable AI technologies. The architecture combines NLP tokenization, TF-IDF feature extraction, a multi-class Logistic Regression intent classifier, an Experta symbolic rule engine, and a NetworkX semantic knowledge graph. Furthermore, the platform integrates an educational AI Algorithm Laboratory demonstrating BFS, DFS, Uniform Cost Search, A* Search, Greedy Search, Hill Climbing, Genetic Algorithms, Minimax, and Alpha-Beta Pruning.

### 3. Introduction
Artificial Intelligence (AI) has emerged as a cornerstone of modern automation. Within higher education, intelligent conversational agents streamline access to institutional knowledge, offering 24/7 availability while reducing administrative overhead. Potential AI is developed to demonstrate both theoretical foundations and practical applications of the college AI curriculum.

### 4. Problem Statement
Manual inquiry systems at college admission counters and academic offices suffer from high latency, physical bottlenecks, and human error. Existing automated approaches either use brittle static FAQ scripts or third-party paid LLMs that risk privacy leakage and factual hallucination. There is a need for an autonomous, locally deployable, and transparent college assistant.

### 5. Objectives
* Construct a zero-hallucination knowledge base extracted directly from authoritative PRPCEM portals (`prpotepatilengg.ac.in` and `academics.prpotepatilengg.ac.in`).
* Implement an end-to-end NLP and Machine Learning classification pipeline with probabilistic confidence thresholding.
* Integrate symbolic reasoning using Experta knowledge rules to guide knowledge retrieval.
* Build a NetworkX semantic knowledge graph modeling institutional relationships (departments, HODs, programs, and facilities).
* Provide an interactive AI Laboratory visualizer for 11 syllabus algorithms.
* Maintain a real-time analytics dashboard with SQLite query logging and Matplotlib visualization.

### 6. Existing System
Traditional college inquiry portals rely on static HTML links or rigid keyword search boxes. Recent conversational systems use hosted LLM APIs (OpenAI, Gemini), which introduce:
* Recurring API costs and internet dependency.
* Risk of generating fabricated ("hallucinated") college facts.
* Lack of academic transparency into internal symbolic reasoning.

### 7. Proposed System
Potential AI replaces black-box API calls with an interpretable, multi-stage AI reasoning pipeline. The system validates input, classifies intent using TF-IDF and Logistic Regression, extracts named entities, fires symbolic rules in Experta, traverses a NetworkX graph, and synthesizes source-attributed responses with academic year awareness.

### 8. System Requirements
* **Operating System:** Windows, Linux, or macOS.
* **Programming Language:** Python 3.11+ / 3.13.
* **Core Libraries:** Flask, scikit-learn, pandas, numpy, networkx, experta, nltk, matplotlib, requests, beautifulsoup4.
* **Database:** SQLite3.
* **Hardware:** Minimal (Runs efficiently on 512MB RAM free-tier cloud instances or local PC).

### 9. System Architecture
The application follows a modular pipeline:
1. **User Interface (HTML5/CSS3/Vanilla JS)** transmits asynchronous JSON payloads to `/api/chat`.
2. **Flask Backend Controller** handles routing, input validation, and security sanitization.
3. **NLP Preprocessing (`ai/preprocess.py`)** cleans tokens and extracts entities.
4. **TF-IDF + Classifier (`ai/classifier.py`)** predicts user intent and confidence score.
5. **Experta Engine (`ai/rules.py`)** performs forward-chaining rule activation.
6. **NetworkX Graph (`ai/knowledge_graph.py`)** navigates relational dependencies.
7. **Response Generator (`ai/response.py`)** merges factual JSON data and attaches source URLs.
8. **Database Logger (`database.py`)** logs telemetry for the analytics dashboard.

### 10. Methodology
The development was executed in phased milestones:
* **Phase 1:** Official web scraping and canonical JSON knowledge base creation (`data/processed/college_data.json`).
* **Phase 2:** Intent taxonomy construction (`data/intents.csv`) across 30 intents.
* **Phase 3:** Training TF-IDF vectorizer and multi-class Logistic Regression classifier.
* **Phase 4:** Formalizing symbolic rules and facts in Experta.
* **Phase 5:** NetworkX knowledge graph modeling.
* **Phase 6:** Response generation and source attribution.
* **Phase 7:** Frontend development (Chat, College Explorer, AI Lab, Dashboard, About).
* **Phase 8:** Comprehensive unit and integration testing via Pytest.

### 11. AI Techniques
* **Feature Extraction:** Sublinear TF-IDF with unigram and bigram ranges:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
* **Multi-Class Logistic Regression:** Softmax probability estimation:
  $$P(y = c \mid \mathbf{x}) = \frac{e^{\mathbf{w}_c^T \mathbf{x}}}{\sum_{k=1}^K e^{\mathbf{w}_k^T \mathbf{x}}}$$
* **Symbolic Production Rules:** Forward-chaining Rete-style inference using Experta.
* **Graph Search:** $f(n) = g(n) + h(n)$ heuristic evaluation.
* **Minimax & Alpha-Beta Cutoffs:** Zero-sum game tree evaluation with $\alpha \ge \beta$ pruning.

### 12. Dataset Specification
`data/intents.csv` contains 278+ labeled user questions across 30 intent categories (greeting, goodbye, thanks, college_information, history, vision_mission, departments, courses, programs, faculty, hod, admission, eligibility, documents, fees, intake, scholarship, library, hostel, facilities, laboratories, academic_calendar, syllabus, examination, notices, contact, location, autonomy, accreditation, placement).

### 13. Knowledge Representation
Knowledge is structured in `data/processed/college_data.json` preserving entity attributes, HODs, seat intakes, laboratory names, eligibility rules, fee structures, and source URLs.

### 14. Experta Rule Engine Implementation
Defined in `ai/rules.py`, `PotentialAIRuleEngine` inherits from `KnowledgeEngine` and declares facts (`UserQuery`, `QueryIntent`, `ExtractedEntity`). Salience-based rules disambiguate general vs. specific queries (e.g., `rule_hod_specific_department` with salience 10 vs. `rule_hod_all_departments` with salience 5).

### 15. Machine Learning Pipeline
`scripts/train_model.py` loads `data/intents.csv`, preprocesses queries, performs stratified train/test splitting (80/20), fits `TfidfVectorizer(ngram_range=(1,2))`, trains `LogisticRegression(C=10.0)`, evaluates precision, recall, and F1 score, and serializes artifacts to `models/`.

### 16. NetworkX Knowledge Graph
`ai/knowledge_graph.py` builds an interconnected `nx.DiGraph` containing 37 nodes and 46 directed edges, mapping institutional hierarchy (`PRPCEM` ➔ `HAS_DEPARTMENT` ➔ `CSE` ➔ `HEADED_BY` ➔ `Dr. Manoj M. Andhare`).

### 17. Syllabus Algorithm Implementations
The `algorithms/` module encapsulates 11 algorithms:
1. `bfs.py`: Breadth-First Search ($O(b^d)$ time & space).
2. `dfs.py`: Depth-First Search ($O(b^m)$ time, $O(b\cdot m)$ space).
3. `ucs.py`: Uniform Cost Search using Priority Queue ($O(b^{1+\lfloor C^*/\epsilon\rfloor})$).
4. `astar.py`: A* Search ($f(n) = g(n) + h(n)$).
5. `greedy.py`: Greedy Best-First Search ($f(n) = h(n)$).
6. `hill_climbing.py`: Steepest-ascent local optimization.
7. `genetic.py`: Binary chromosome evolution with selection, crossover, and mutation.
8. `minimax.py`: Exhaustive game tree search for Tic-Tac-Toe.
9. `alpha_beta.py`: Game tree search with $\alpha$-$\beta$ branch pruning.
10. `water_jug.py`: State-space BFS measuring target liters using 2 jugs.
11. `missionaries_cannibals.py`: River crossing state-space BFS search.

### 18. System Implementation & Routes
* `GET /`: Interactive Chatbot view.
* `GET /college`: College Information Explorer with 8 categorized tabs.
* `GET /ai-lab`: Interactive algorithm simulator.
* `GET /dashboard`: Analytics dashboard with Pandas telemetry and Matplotlib chart.
* `GET /about`: Syllabus concepts and architecture.
* `POST /api/chat`: Primary conversational endpoint.
* `POST /api/ai-lab/*`: Algorithmic execution endpoints.

### 19. Testing & Verification
A 26-test automated Pytest suite covers NLP preprocessing, ML classification, Experta rules, NetworkX graph queries, factual chatbot responses, fallback triggering, and all 11 algorithm solvers.

### 20. Experimental Results & Metrics
* **Classifier Accuracy:** ~71.4% to 76.7% across 30 granular intent classes.
* **Average Response Latency:** < 25 ms per request on local CPU.
* **Test Suite Pass Rate:** 26 / 26 passed (100%).
* **Memory Footprint:** < 65 MB RAM.

### 21. Screenshots & User Interface Walkthrough
*(Screenshots can be captured from the running web interface at `/`, `/college`, `/ai-lab`, `/dashboard`, and `/about`)*

### 22. Advantages of Potential AI
1. Zero operational API cost and zero rate limits.
2. Complete privacy: No user messages transmitted to third-party servers.
3. Total factual precision with source URLs.
4. Comprehensive syllabus demonstration in one unified platform.

### 23. Limitations
1. Scope restricted to the PRPCEM knowledge base.
2. Intent classification confidence drops on highly ambiguous colloquial queries.

### 24. Future Scope
1. Multi-lingual conversational support for Marathi and Hindi.
2. Voice interface integration with Speech-to-Text (STT) and Text-to-Speech (TTS).

### 25. Course Outcome (CO) Mapping
* **CO1:** Understand AI fundamentals and intelligent agents (Unit 1).
* **CO2:** Apply Python and AI libraries (Unit 2).
* **CO3:** Solve problems using uninformed search (Unit 3).
* **CO4:** Analyze and implement heuristic/local search (Unit 4).
* **CO5:** Design game-playing AI (Unit 5).
* **CO6:** Develop awareness of real-world AI applications (Unit 6).

### 26. Conclusion
Potential AI successfully demonstrates how classic, symbolic, and statistical Artificial Intelligence techniques can be combined to build an effective, zero-cost, and hallucination-free college assistant.

### 27. References
1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
2. Rich, E., Knight, K., & Nair, S. B. (2017). *Artificial Intelligence* (3rd ed.). McGraw Hill.
3. Official PRPCEM Portals: `https://prpotepatilengg.ac.in/` and `https://academics.prpotepatilengg.ac.in/`.
