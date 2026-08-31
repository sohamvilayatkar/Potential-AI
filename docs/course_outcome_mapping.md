# POTENTIAL AI - Course Outcome (CO) Mapping
## Artificial Intelligence Mini-Project Syllabus Alignment

**Target Institution:** P. R. Pote Patil College of Engineering & Management, Amravati  
**Course Code:** AI Mini-Project  
**Academic Year:** 2025-26 / 2026-27  

---

### Course Outcomes Matrix

| Course Outcome (CO) | Syllabus Unit | Theoretical Competency | Practical Demonstration in POTENTIAL AI |
| :--- | :--- | :--- | :--- |
| **CO1** | **Unit 1 – Introduction to AI & Agents** | Formulate problem definitions, characterize environment types, and define intelligent agent architectures. | • Formal PEAS specification for Potential AI assistant.<br>• Detailed environment characterization (partially observable, deterministic, sequential, static, discrete).<br>• Educational evaluation of the Turing Test and task-oriented vs. general AI. |
| **CO2** | **Unit 2 – Python for Artificial Intelligence** | Apply Python AI libraries for symbolic reasoning, data processing, machine learning, and knowledge representation. | • NumPy & Pandas for data manipulation & telemetry analysis.<br>• Matplotlib for dynamic server-side intent distribution chart generation.<br>• NetworkX for semantic directed knowledge graph representation.<br>• Experta for declarative forward-chaining rule inference.<br>• scikit-learn & NLTK for text preprocessing, TF-IDF vectorization, and intent classification. |
| **CO3** | **Unit 3 – Uninformed Search & Problem Solving** | Implement state-space formulations, tree/graph search strategies, and solve classic combinatorial AI problems. | • Breadth-First Search (BFS) graph pathfinder.<br>• Depth-First Search (DFS) exploration simulator.<br>• Uniform Cost Search (UCS) priority-queue cost optimizer.<br>• Water Jug Problem solver using state transitions and Extended Euclidean / GCD solvability.<br>• Missionaries and Cannibals river-crossing BFS solver. |
| **CO4** | **Unit 4 – Informed Search & Heuristic Optimization** | Design admissible and consistent heuristics, implement best-first search, and apply local/evolutionary optimization. | • A* Search evaluating $f(n) = g(n) + h(n)$ with admissible Euclidean distances.<br>• Greedy Best-First Search evaluating $f(n) = h(n)$.<br>• Steepest-Ascent Hill Climbing with neighborhood delta tracing and local peak detection.<br>• Genetic Algorithm (GA) evolutionary optimizer with binary chromosomes, roulette wheel selection, single-point crossover, and bit-flip mutation. |
| **CO5** | **Unit 5 – Adversarial Search & Game Playing** | Model zero-sum two-player games, construct game trees, and optimize game evaluation using branch pruning. | • Minimax game tree evaluation algorithm for Tic-Tac-Toe.<br>• Alpha-Beta Pruning ($\alpha \ge \beta$) search engine.<br>• Real-time comparative analytics demonstrating branch cutoffs and reduction in explored game-tree nodes. |
| **CO6** | **Unit 6 – Real-World AI Applications & Ethics** | Design, deploy, and critically evaluate an end-to-end AI software system while analyzing ethical considerations, benefits, and risks. | • Complete web-based college assistant delivering factual PRPCEM answers with official source URLs.<br>• Zero-hallucination confidence thresholding.<br>• SQLite query logging and real-time performance dashboard.<br>• Comprehensive analysis of AI benefits, risks, and educational limitations. |

---

### Unit-by-Unit Implementation Traceability

#### Unit 1: Introduction to AI & Intelligent Agents
* **PEAS Specification:** Defined in `templates/about.html` and `docs/project_report.md`.
* **Agent Architecture:** User Query $\rightarrow$ Perception $\rightarrow$ Multi-Tier Reasoning $\rightarrow$ Action $\rightarrow$ Grounded Answer.
* **Turing Test Foundation:** Evaluated in educational modules clarifying task-oriented systems vs. unrestricted AGI.

#### Unit 2: Python for AI & Knowledge Representation
* **Symbolic Reasoning:** `ai/rules.py` implements `PotentialAIRuleEngine(KnowledgeEngine)` with salience and facts (`UserQuery`, `QueryIntent`, `ExtractedEntity`, `CollegeAction`).
* **Semantic Graph:** `ai/knowledge_graph.py` implements a directed graph (`nx.DiGraph`) with 37 entity nodes and 46 relational edges.
* **Vectorization:** `ai/preprocess.py` and `ai/classifier.py` use `TfidfVectorizer(ngram_range=(1,2))` and `LogisticRegression`.

#### Unit 3: Uninformed Search Strategies
* **BFS:** `algorithms/bfs.py` (FIFO Queue, $O(b^d)$ time/space, complete & optimal for uniform costs).
* **DFS:** `algorithms/dfs.py` (LIFO Stack, $O(b^m)$ time, $O(bm)$ space).
* **UCS:** `algorithms/ucs.py` (Priority Queue, $O(b^{1+\lfloor C^*/\epsilon\rfloor})$).
* **Water Jug:** `algorithms/water_jug.py` (State-space BFS exploring 6 fill/empty/pour operators).
* **Missionaries & Cannibals:** `algorithms/missionaries_cannibals.py` (State-space BFS ensuring legal river crossing).

#### Unit 4: Informed & Local Search
* **A\* Search:** `algorithms/astar.py` ($f(n) = g(n) + h(n)$, priority queue, admissible heuristic).
* **Greedy Search:** `algorithms/greedy.py` ($f(n) = h(n)$).
* **Hill Climbing:** `algorithms/hill_climbing.py` (Maximizing $f(x) = -(x-4)^2 + 25 + 3\sin(2x)$).
* **Genetic Algorithm:** `algorithms/genetic.py` (Evolutionary cycle over binary bit strings).

#### Unit 5: Game Playing & Adversarial Search
* **Minimax:** `algorithms/minimax.py` (Game tree backtracking for optimal Tic-Tac-Toe moves).
* **Alpha-Beta Pruning:** `algorithms/alpha_beta.py` (Pruning branches where $\beta \le \alpha$).
* **Visual Comparison:** `templates/ai_lab.html` and `static/js/ai_lab.js` rendering evaluated vs. pruned nodes.

#### Unit 6: Real-World AI Application & Deployment
* **Full-Stack Assistant:** Flask web application (`app.py`), REST API (`POST /api/chat`), responsive HTML/CSS/JS frontend.
* **Database Telemetry:** SQLite logging (`database.py`) and Matplotlib intent distribution analytics (`templates/dashboard.html`).
* **Production Readiness:** Configured for cloud deployment via `Procfile`, `runtime.txt`, dynamic `PORT`, and 0.0.0.0 binding.
