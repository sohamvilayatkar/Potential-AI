# POTENTIAL AI - Comprehensive Viva Voce Question Bank
## 50+ In-Depth Questions & Student-Friendly Answers for Mini-Project Evaluation

---

### Section 1: AI Fundamentals & Intelligent Agents (Unit 1)

#### Q1: What is Artificial Intelligence, and what kind of AI is POTENTIAL AI?
**Answer:** Artificial Intelligence is the study and design of intelligent agents that perceive their environment and take actions to maximize their chance of successfully achieving goals. POTENTIAL AI is a **Domain-Specific Task-Oriented Intelligent Agent** that combines statistical Natural Language Processing, Machine Learning, Symbolic Expert Systems (Experta), and Semantic Knowledge Graphs (NetworkX) to provide factual college information without relying on third-party cloud APIs.

#### Q2: What is an Intelligent Agent in AI theory?
**Answer:** An intelligent agent is anything that can perceive its environment through **sensors** and act upon that environment through **actuators** in pursuit of specific goals.

#### Q3: Define the PEAS specification for POTENTIAL AI.
**Answer:**
* **Performance Measure (P):** Factual correctness of college details, zero hallucination rate, intent classification accuracy, request latency (<50ms), and official source link validity.
* **Environment (E):** Student and visitor queries via the web browser; PRPCEM official web knowledge base.
* **Actuators (A):** Synthesized natural text responses, clickable source URL links, prompt chips, and UI status updates.
* **Sensors (S):** HTTP POST requests carrying JSON text payloads (`/api/chat`).

#### Q4: Describe the nature of the environment for POTENTIAL AI.
**Answer:**
* **Partially Observable:** The user's underlying intent must be inferred from variable natural language text.
* **Deterministic:** For any specific query and knowledge state, the agent generates a consistent, factual answer.
* **Sequential:** The user and agent interact across consecutive conversation turns.
* **Static:** The internal college knowledge base remains unchanged during a single query inference cycle.
* **Discrete:** Intents, entity classes, and graph nodes are represented as finite discrete categories.
* **Single-Agent:** Potential AI operates as the autonomous decision-making entity.

#### Q5: What is the Turing Test? Does Potential AI pass it?
**Answer:** Proposed by Alan Turing in 1950, the Turing Test evaluates whether a machine's conversational behavior is indistinguishable from a human across unrestricted topics. Potential AI is deliberately a **task-specific college assistant**, not an Artificial General Intelligence (AGI). It purposely restricts answers to PRPCEM college facts and triggers a safe fallback on unrelated questions rather than pretending to possess human consciousness.

---

### Section 2: Natural Language Processing & TF-IDF (Unit 2 & 6)

#### Q6: What is NLP Preprocessing, and why is it necessary?
**Answer:** NLP preprocessing transforms messy raw user text into clean, standardized tokens suitable for mathematical modeling. The steps in `ai/preprocess.py` include:
1. Converting text to lowercase.
2. Stripping punctuation and special symbols.
3. Collapsing extra whitespace.
4. Tokenization into word units.
5. Stemming/lemmatization to reduce words to their root forms (e.g., "admissions" $\rightarrow$ "admiss").

#### Q7: What is TF-IDF and how is it calculated?
**Answer:** **TF-IDF (Term Frequency - Inverse Document Frequency)** evaluates how important a word is to a specific document within a larger collection.
$$\text{TF}(t, d) = \frac{\text{Count of } t \text{ in } d}{\text{Total words in } d}$$
$$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

#### Q8: Why is TF-IDF superior to simple Bag-of-Words (CountVectorizer)?
**Answer:** CountVectorizer simply counts raw frequencies, giving high weights to common non-informative words (like "college", "is", "the"). TF-IDF penalizes words that appear across all documents and gives higher weights to unique, discriminatory keywords (e.g., "hod", "syllabus", "fees", "scholarship").

#### Q9: What are N-grams and why did you use `ngram_range=(1, 2)`?
**Answer:** An N-gram is a contiguous sequence of $N$ tokens. Unigrams ($N=1$) capture single words ("computer"), while bigrams ($N=2$) capture two-word phrases ("computer engineering", "fee structure"). Using `ngram_range=(1, 2)` allows the model to differentiate "computer engineering" from "mechanical engineering".

---

### Section 3: Machine Learning & Intent Classification (Unit 2 & 6)

#### Q10: Why did you choose Logistic Regression for intent classification?
**Answer:**
1. **Calibrated Probabilities:** Logistic Regression outputs genuine softmax probabilities, enabling confidence thresholding.
2. **Computational Efficiency:** Trains in < 2 seconds on a standard CPU and consumes < 50MB RAM.
3. **Interpretability:** Feature weights can be directly inspected to understand which keywords drove the prediction.
4. **Zero Recurring Costs:** Runs entirely offline without expensive GPU servers or cloud API bills.

#### Q11: How does Logistic Regression calculate multi-class probabilities?
**Answer:** It applies the **Softmax function** over linear decision boundaries:
$$P(y = c \mid \mathbf{x}) = \frac{e^{\mathbf{w}_c^T \mathbf{x} + b_c}}{\sum_{k=1}^K e^{\mathbf{w}_k^T \mathbf{x} + b_k}}$$

#### Q12: What is the purpose of the Confidence Threshold?
**Answer:** If the highest predicted probability is below `CONFIDENCE_THRESHOLD` (e.g., 0.35) and no recognized college entities exist in the query, Potential AI avoids guessing and safely triggers the **Fallback Rule**, directing the user to official sources.

#### Q13: What evaluation metrics did you use to assess model performance?
**Answer:**
* **Accuracy:** Percentage of correctly classified intents across the test set.
* **Precision:** $\frac{TP}{TP + FP}$ (Exactness of predicted intents).
* **Recall:** $\frac{TP}{TP + FN}$ (Completeness of retrieved intents).
* **F1 Score:** Harmonic mean of precision and recall: $2 \times \frac{P \times R}{P + R}$.

---

### Section 4: Named Entity Recognition & Knowledge Retrieval (Unit 2)

#### Q14: How does Named Entity Recognition (NER) work in Potential AI?
**Answer:** In `ai/entities.py`, regex patterns with strict word boundaries (`\b...\b`) extract recognized institutional entities:
* **Departments:** CSE, CSE (AIML), AI&DS, Civil, Mechanical, Electrical, EXTC, First Year, MBA, MCA.
* **Degree Programs:** B.Tech, M.Tech, MBA, MCA.
* **Academic Years:** 2025-26, 2026-27.
* **Information Types:** HOD, Fees, Admissions, Documents, Facilities, Syllabus.

#### Q15: How does Potential AI avoid false positives on short words like "me"?
**Answer:** We enforce strict word boundary and phrase contextualization (e.g., `mech|mechanical|me\s+dept|me\s+branch`) so that normal English sentences containing the pronoun "me" (e.g., "Tell me about...") do not accidentally trigger the Mechanical Engineering department entity.

#### Q16: How is the knowledge base structured in `college_data.json`?
**Answer:** It stores structured JSON objects categorized into `college`, `departments`, `programs`, `admissions`, `fees`, `facilities`, `academic`, `notices`, `contact`, and `sources`. Every record preserves official source URLs and academic year tags.

---

### Section 5: Experta Symbolic Rule Engine (Unit 2)

#### Q17: What is Experta and what role does it play in this project?
**Answer:** Experta is a Python-based production rule engine modeled after CLIPS. While Machine Learning provides statistical intent predictions, **Experta performs symbolic, logical forward-chaining inference** to determine the precise institutional action required (e.g., deciding whether to lookup a specific department HOD or list all HODs).

#### Q18: What are Facts, Rules, and KnowledgeEngine in Experta?
**Answer:**
* **Facts:** Declarations asserting current knowledge state (`UserQuery`, `QueryIntent`, `ExtractedEntity`).
* **Rules:** Condition-action pairs (`@Rule(...)`) that execute when pattern conditions are met in the working memory.
* **KnowledgeEngine:** The core inference engine managing fact matching, agenda scheduling, conflict resolution, and execution.

#### Q19: How does Salience work in Experta?
**Answer:** Salience is an integer priority assigned to rules. When multiple rules match simultaneously, the rule with the highest salience fires first (e.g., `rule_hod_specific_department` with salience 10 fires before `rule_hod_all_departments` with salience 5).

#### Q20: How did you make Experta compatible with Python 3.10+ / 3.13?
**Answer:** Classic Experta imports abstract collections from `collections.Mapping`, which was relocated to `collections.abc.Mapping` in modern Python. We implemented compatibility shims at the top of `ai/rules.py`:
```python
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
```

---

### Section 6: NetworkX Semantic Knowledge Graph (Unit 2)

#### Q21: What is a Knowledge Graph and why is NetworkX used?
**Answer:** A Knowledge Graph represents real-world entities as **nodes** and their semantic relationships as **directed edges**. NetworkX (`nx.DiGraph`) models the PRPCEM ecosystem (37 nodes, 46 edges) allowing multi-hop relationship discovery (e.g., traversing from `PRPCEM` ➔ `HAS_DEPARTMENT` ➔ `CSE` ➔ `HEADED_BY` ➔ `Dr. Manoj M. Andhare`).

#### Q22: Give an example of a graph traversal query in Potential AI.
**Answer:** When asked "Who is the HOD of Computer Engineering?", the system looks up node `cse`, follows the outbound edge labeled `HEADED_BY`, and retrieves node `Dr. Manoj M. Andhare`.

---

### Section 7: Uninformed Search Algorithms (Unit 3)

#### Q23: Explain Breadth-First Search (BFS).
**Answer:** BFS explores nodes layer by layer using a FIFO queue.
* **Time Complexity:** $O(b^d)$, **Space Complexity:** $O(b^d)$.
* **Completeness:** Yes; **Optimality:** Yes for uniform step costs.

#### Q24: Explain Depth-First Search (DFS).
**Answer:** DFS explores as deep as possible along each branch before backtracking using a LIFO stack.
* **Time Complexity:** $O(b^m)$, **Space Complexity:** $O(b \cdot m)$.
* **Completeness:** No (can loop in cycles); **Optimality:** No.

#### Q25: Explain Uniform Cost Search (UCS).
**Answer:** UCS expands the node with the lowest cumulative path cost $g(n)$ using a Priority Queue (`heapq`).
* **Time & Space:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$.
* **Completeness & Optimality:** Guaranteed optimal for non-negative step costs.

#### Q26: How is the Water Jug Problem formulated in AI?
**Answer:**
* **State:** Tuple $(x, y)$ representing current liters in Jug A and Jug B.
* **Start:** $(0, 0)$; **Goal:** $(x, y)$ where $x = \text{target}$ or $y = \text{target}$.
* **Operators:** 6 actions (Fill A, Fill B, Empty A, Empty B, Pour A to B, Pour B to A).
* **Search:** BFS state-space search finding the minimum state transitions.

#### Q27: How is the Missionaries and Cannibals problem formulated?
**Answer:**
* **State:** $(M_{left}, C_{left}, Boat_{pos})$.
* **Safety Condition:** $M \ge C$ on both banks whenever $M > 0$.
* **Search:** BFS exploring safe boat trips carrying 1 or 2 people.

---

### Section 8: Informed & Heuristic Search Algorithms (Unit 4)

#### Q28: What is A* Search and how does it work?
**Answer:** A* Search evaluates nodes using $f(n) = g(n) + h(n)$, combining exact cost from start $g(n)$ with estimated heuristic cost to goal $h(n)$.

#### Q29: What makes a heuristic Admissible and Consistent?
**Answer:**
* **Admissible:** $h(n) \le h^*(n)$ (never overestimates the true cost to reach the goal).
* **Consistent (Monotone):** $h(n) \le c(n, a, n') + h(n')$ (satisfies the triangle inequality).

#### Q30: How does Greedy Best-First Search differ from A*?
**Answer:** Greedy Best-First Search uses $f(n) = h(n)$ only. It is fast but non-optimal because it ignores the cost already incurred $g(n)$.

#### Q31: What is Hill Climbing and what are its main limitations?
**Answer:** Hill Climbing is a local search optimization algorithm that continuously moves in the direction of steepest ascent. Its limitations are local maxima (false peaks), plateaus (flat gradients), and ridges.

#### Q32: Explain the main stages of a Genetic Algorithm.
**Answer:**
1. **Initial Population:** Set of candidate binary chromosomes.
2. **Fitness Evaluation:** Scoring quality via objective function.
3. **Selection:** Roulette wheel selection biased toward fitter individuals.
4. **Crossover:** Recombining pairs of chromosomes at split points.
5. **Mutation:** Random bit-flips with small probability ($p_m = 0.05$).
6. **Replacement:** Creating the next generation.

---

### Section 9: Game Playing & Adversarial Search (Unit 5)

#### Q33: How does the Minimax algorithm work in Tic-Tac-Toe?
**Answer:** Minimax evaluates game tree states by recursively assuming the Maximizer (AI) maximizes the payoff while the Minimizer (Human) minimizes it, returning $+10-\text{depth}$ for AI win, $\text{depth}-10$ for Human win, and $0$ for Draw.

#### Q34: What is Alpha-Beta Pruning and how does it improve Minimax?
**Answer:** Alpha-Beta Pruning maintains thresholds $\alpha$ (best Maximizer score) and $\beta$ (best Minimizer score). If at any node $\beta \le \alpha$, further exploration of that subtree is pruned because it cannot affect the final minimax decision. This reduces the branching factor from $b$ to $\approx \sqrt{b}$.

---

### Section 10: System Design, Database & Telemetry (Units 2 & 6)

#### Q35: How does the SQLite database support analytics?
**Answer:** Every query received by `/api/chat` is stored in `queries_log` (id, timestamp, user_message, intent, confidence, response_status). `database.py` aggregates metrics using Pandas and renders Matplotlib charts for the live dashboard.

#### Q36: How does Potential AI prevent SQL Injection?
**Answer:** By utilizing parameterized queries (`cursor.execute("INSERT ... VALUES (?, ?, ?, ?)", (msg, intent, conf, status))`) where user input is treated strictly as data literals.

#### Q37: How does Potential AI prevent Cross-Site Scripting (XSS)?
**Answer:** In `static/js/chatbot.js`, all user text passes through `escapeHTML()` before being inserted into the DOM.

---

### Section 11: Factual Accuracy & Source Attribution

#### Q38: What is the "Zero-Hallucination" guarantee?
**Answer:** Potential AI only answers using records present in `data/processed/college_data.json` extracted from official PRPCEM web portals. If a requested fact is not present, it explicitly states it could not find the information rather than generating plausible falsehoods.

#### Q39: How are official source URLs attached to responses?
**Answer:** Every response returned by `ai/response.py` contains a `sources` array with exact official URLs (e.g., `https://prpotepatilengg.ac.in/admission`) rendered as clickable external links in the UI.

#### Q40: How is the Academic Year handled?
**Answer:** Admission rules and fee records are explicitly tagged with academic years (`2025-26` or `2026-27`) to clarify information currency to students.

---

### Section 12: Deployment, Ethics & Viva Demonstration

#### Q41: How is the project deployed on free Python hosts?
**Answer:** The project binds to `0.0.0.0` with dynamic environment variable `PORT`, includes a `Procfile` (`web: gunicorn app:app`), `runtime.txt`, and requires only open-source Python libraries with zero paid external APIs.

#### Q42: What are the primary benefits of AI in college administration?
**Answer:** 24/7 instant accessibility, elimination of physical queues for routine FAQs, reduction in administrative workload, and consistent, grounded answers.

#### Q43: What are the primary risks of AI in education, and how does Potential AI mitigate them?
**Answer:**
* **Risk:** Hallucinations / Fake information $\rightarrow$ *Mitigated by strict knowledge base grounding and confidence fallbacks.*
* **Risk:** Over-reliance $\rightarrow$ *Mitigated by direct clickable links to official PRPCEM circulars and PDFs.*
* **Risk:** Privacy leakage $\rightarrow$ *Mitigated by 100% local on-device intelligence without transmitting user chats to commercial LLM providers.*

#### Q44: What is the purpose of the "AI Details" toggle in the chat interface?
**Answer:** It makes the multi-tier reasoning pipeline transparent for academic examiners by displaying the predicted Intent, Confidence score, Extracted Entities, Experta Rule name, and Knowledge Engine action.

#### Q45: How can official data be updated when college notices change?
**Answer:** Administrators execute `python scripts/scrape_website.py`, then `python scripts/process_data.py`, and `python scripts/train_model.py`.

#### Q46: What is the role of Flask in this application?
**Answer:** Flask serves as the lightweight WSGI backend controller providing web routing (`GET /`, `/college`, `/ai-lab`, `/dashboard`, `/about`) and RESTful JSON APIs (`POST /api/chat`, `/api/ai-lab/*`).

#### Q47: Why is the AI Algorithm Lab a crucial part of this mini-project?
**Answer:** It provides interactive educational simulators for all 11 algorithms in the AI syllabus, bridging theoretical algorithmic knowledge with interactive visual implementations.

#### Q48: What is the total number of test cases in the test suite?
**Answer:** 37 automated Pytest unit and integration tests covering preprocessing, intent classification, entity extraction, knowledge retrieval, Experta rules, NetworkX graph traversals, chatbot responses, and search/game algorithms.

#### Q49: What are the current limitations of Potential AI?
**Answer:** Its knowledge is bounded by the PRPCEM institutional domain and it currently operates in English text only.

#### Q50: What is the future scope of Potential AI?
**Answer:** Adding multi-lingual support (Marathi and Hindi translation layers), voice input/output speech interfaces, and automated synchronization with SGBAU university exam result servers.
