# POTENTIAL AI

> **An Intelligent Web-Based College Assistant Chatbot**  
> For **P. R. Pote Patil College of Engineering & Management (PRPCEM), Amravati**  
> *(Autonomous Institute • NAAC 'A' Grade • DTE Code: 1107 • SGBAU Affiliated)*

---

## 📌 Project Overview
**POTENTIAL AI** is a comprehensive academic Artificial Intelligence mini-project that implements a local, privacy-preserving intelligent chatbot assistant for P. R. Pote Patil College of Engineering & Management, Amravati.

Unlike commercial chatbots that rely on paid external LLM APIs (such as OpenAI, Gemini, or Claude), **Potential AI** derives 100% of its intelligence from transparent, syllabus-aligned AI techniques:
* **Natural Language Processing (NLP)** tokenization, normalization, and entity extraction.
* **TF-IDF (Term Frequency - Inverse Document Frequency)** feature vectorization.
* **Machine Learning Intent Classification** (Logistic Regression with multi-class probability scoring).
* **Experta Symbolic Rule Engine** for forward-chaining rule-based logical inference.
* **NetworkX Knowledge Graph** for semantic graph modeling and relationship traversal.
* **Classical AI Search & Optimization Algorithms** (BFS, DFS, UCS, A*, Greedy, Hill Climbing, Genetic Algorithm, Minimax, and Alpha-Beta Pruning).
* **Voice Interaction & Accessibility:** Native client-side Speech-to-Text (STT via Web Speech API) and Text-to-Speech (TTS with auto-speak and read-aloud controls) without any paid API keys or audio latency.
* **Strict Fact Grounding & Source Attribution** referencing authoritative PRPCEM official web portals (`https://prpotepatilengg.ac.in/` and `https://academics.prpotepatilengg.ac.in/`).

---

## 🎯 Problem Statement & Objectives
### Problem Statement
Prospective students, parents, and enrolled scholars frequently need fast, accurate information regarding admissions, eligibility, fee structures, scholarships, departments, faculty heads, and academic calendars. Relying on manual office inquiries causes delays and repetitive administrative workload.

### Key Objectives
1. **Zero Hallucination Guarantee:** Ground all factual responses strictly in verified, structured official PRPCEM knowledge with direct source attribution.
2. **Transparent Academic AI:** Demonstrate core units of the Artificial Intelligence syllabus through an interactive web platform and algorithm laboratory.
3. **No External LLM / Zero Recurring Cost:** Operate completely offline or on free cloud hosting without external API keys or subscription fees.
4. **Interactive AI Lab & Analytics:** Provide interactive visualizers for 11 AI algorithms and a live dashboard with SQLite telemetry and Matplotlib analytics.

---

## 🏛️ Official Data Sources
The knowledge base is built from official PRPCEM domains:
* **Main College Portal:** `https://prpotepatilengg.ac.in/` (Establishment, trust, governance, departments, intake, facilities, contact)
* **Dean (Academics) Portal:** `https://academics.prpotepatilengg.ac.in/` (Academic calendars, autonomous syllabus schemes, notices)
* **Autonomous Academic Regulations:** `https://academics.prpotepatilengg.ac.in/PRPCEM_Ordinance_23-24_DraftCopy.pdf`
* **Online Examination Portal:** `https://prpcem.dotcominfotech.in/`

---

## 🏗️ System Architecture

```
                         USER
                           │
                           ▼
                  ┌────────────────┐
                  │  Web Interface │
                  │  (HTML/CSS/JS) │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Flask Backend  │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Input Validate │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ NLP Preprocess │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ TF-IDF Vector  │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ ML Classifier  │ ──► Intent & Confidence
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Entity Extract │ ──► Department, Program, Academic Year
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  Experta Rules │ ──► Forward-Chaining Inference
                  └────────┬───────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
         ┌────────────────┐ ┌────────────────┐
         │ Knowledge Base │ │ NetworkX Graph │
         │ (college_data) │ │ (Entity Nodes) │
         └────────┬───────┘ └────────┬───────┘
                  └────────┬────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Response Gen.  │
                  └────────┬───────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Source Attrib. │
                  └────────┬───────┘
                           │
                           ▼
                         USER
```

---

## 🧠 AI Syllabus & Course Outcome (CO) Mapping

| Course Outcome | Syllabus Unit | Demonstration in Potential AI |
| :--- | :--- | :--- |
| **CO1** | Unit 1 – Intro to AI & Agents | PEAS Intelligent Agent modeling, Environment Analysis, and Turing Test foundation. |
| **CO2** | Unit 2 – Python for AI | Python, NumPy, Pandas, Matplotlib, NetworkX, Experta, and scikit-learn. |
| **CO3** | Unit 3 – Uninformed Search | Breadth-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS), Water Jug Solver, and Missionaries & Cannibals. |
| **CO4** | Unit 4 – Informed & Local Search | A* Search ($f=g+h$), Greedy Best-First Search ($f=h$), Hill Climbing, and Genetic Algorithm. |
| **CO5** | Unit 5 – Game Playing | Unbeatable Tic-Tac-Toe game engine powered by Minimax and Alpha-Beta Pruning. |
| **CO6** | Unit 6 – AI Applications | Real-world conversational college assistant, SQLite telemetry, and analytics dashboard. |

---

## 🛠️ Technology Stack

* **Backend:** Python 3.11+ / 3.13, Flask, Gunicorn
* **Frontend:** HTML5, CSS3 (Custom Dark/Light Slate AI Theme), Vanilla JavaScript (No heavy frameworks)
* **Machine Learning & NLP:** scikit-learn, NLTK, TF-IDF Vectorizer, Logistic Regression
* **Expert Systems & Rules:** Experta (with collections.abc shims for modern Python support)
* **Knowledge Representation:** NetworkX Directed Graph (`nx.DiGraph`), Structured JSON Knowledge Base
* **Data Processing & Visualization:** Pandas, NumPy, Matplotlib
* **Database & Telemetry:** SQLite3

---

## 📁 Project Structure

```
potential-ai/
│
├── app.py                      # Main Flask application & API routes
├── config.py                   # Configuration & environment variables
├── database.py                 # SQLite logging & Pandas analytics
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment execution command
├── runtime.txt                 # Python runtime version
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete project documentation
│
├── ai/                         # Artificial Intelligence Core Modules
│   ├── __init__.py
│   ├── preprocess.py           # Text normalization & entity extraction
│   ├── classifier.py           # TF-IDF + Logistic Regression Intent Classifier
│   ├── rules.py                # Experta forward-chaining rule engine
│   ├── knowledge_graph.py      # NetworkX semantic knowledge graph
│   └── response.py             # 12-step AI response generator & source attribution
│
├── algorithms/                 # Syllabus AI Algorithms Library
│   ├── __init__.py
│   ├── bfs.py                  # Breadth-First Search
│   ├── dfs.py                  # Depth-First Search
│   ├── ucs.py                  # Uniform Cost Search
│   ├── astar.py                # A* Heuristic Search
│   ├── greedy.py               # Greedy Best-First Search
│   ├── hill_climbing.py        # Steepest Ascent Hill Climbing
│   ├── genetic.py              # Genetic Algorithm Evolutionary Optimizer
│   ├── minimax.py              # Minimax Game Tree Evaluation
│   ├── alpha_beta.py           # Alpha-Beta Pruning Game Tree Engine
│   ├── water_jug.py            # Water Jug State-Space Search Solver
│   └── missionaries_cannibals.py # Missionaries & Cannibals Solver
│
├── data/                       # Ground Truth Knowledge Data
│   ├── raw/                    # Scraped raw web data
│   ├── processed/
│   │   └── college_data.json   # Canonical structured PRPCEM knowledge base
│   ├── intents.csv             # Intent training dataset (278+ examples, 30 intents)
│   ├── sources.json            # Authoritative source catalog with URLs & metadata
│   └── potential_ai.db         # SQLite telemetry database
│
├── models/                     # Trained Serialized Machine Learning Artifacts
│   ├── vectorizer.pkl          # Pickled TF-IDF Vectorizer
│   └── intent_model.pkl        # Pickled Logistic Regression Classifier
│
├── scripts/                    # Maintenance & Pipeline Automation Scripts
│   ├── scrape_website.py       # Scrapes official PRPCEM web portals
│   ├── process_data.py         # Transforms raw data into canonical JSON knowledge base
│   ├── train_model.py          # Trains and evaluates ML classifier
│   └── init_database.py        # Initializes and seeds SQLite database
│
├── templates/                  # Frontend Jinja2 HTML Templates
│   ├── base.html               # Base layout with sidebar and branding
│   ├── index.html              # Interactive Chatbot interface
│   ├── college.html            # PRPCEM College Information Explorer
│   ├── ai_lab.html             # Interactive AI Algorithms Laboratory
│   ├── dashboard.html          # Analytics Dashboard & Matplotlib charts
│   └── about.html              # AI Concepts, Architecture & Syllabus Mapping
│
├── static/                     # Frontend Assets
│   ├── css/
│   │   └── style.css           # Modern, responsive AI styling
│   └── js/
│       ├── chatbot.js          # Chatbot UI interaction & markdown formatting
│       ├── ai_lab.js           # Interactive solvers & Tic-Tac-Toe engine
│       └── dashboard.js        # Auto-refreshing dashboard analytics
│
├── tests/                      # Automated Pytest Suite
│   ├── conftest.py             # Pytest configuration
│   ├── test_preprocess.py      # Unit tests for NLP preprocessing
│   ├── test_classifier.py      # Unit tests for intent classification
│   ├── test_rules.py           # Unit tests for Experta rule engine
│   ├── test_knowledge_graph.py # Unit tests for NetworkX graph
│   ├── test_chatbot.py         # Unit tests for response generator & fallback
│   ├── test_algorithms.py      # Unit tests for all 11 AI algorithms
│   └── test_web_routes.py      # Integration tests for Flask web routes & APIs
│
└── docs/                       # Academic Submission Documentation
    ├── project_report.md       # Full 27-section comprehensive project report
    └── viva_questions.md       # 35+ Viva preparation questions and answers
```

---

## ⚡ Installation & Local Execution

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/potential-ai.git
cd potential-ai
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Verify Trained Models
```bash
python scripts/init_database.py
python scripts/train_model.py
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 🔄 Data Ingestion & Update Workflow

If official college information changes (e.g., new academic year notices or fees):
1. **Scrape Authoritative Websites:**
   ```bash
   python scripts/scrape_website.py
   ```
2. **Process and Verify Structured Data:**
   ```bash
   python scripts/process_data.py
   ```
3. **Retrain Intent Classifier (if intents updated):**
   ```bash
   python scripts/train_model.py
   ```
4. **Restart the Application.**

---

## 🤖 Telegram Bot Integration & Flying Button

Potential AI includes full Telegram bot support, allowing students and visitors to chat with the AI assistant directly via Telegram:

### 1. Telegram Bot Features
* **Zero External LLMs:** Powered by the exact same local inference pipeline (NLP, TF-IDF, Logistic Regression, Experta, NetworkX).
* **Official Source Attribution:** Automatically attaches official PRPCEM links to Telegram replies.
* **Dual Operation Modes:**
  * **Webhook Mode (`POST /api/telegram/webhook`):** Production-ready endpoint for cloud hosting with HTTPS.
  * **Standalone Polling (`python platforms/telegram_bot.py`):** For local testing without needing a public domain.
* **Floating Web Button:** A floating action button (FAB) with levitation animation and pulse aura appears on all web pages, linking directly to the bot (`https://t.me/PRPCEM_PotentialAI_Bot`).

### 2. Configuration & Running Telegram Bot
1. Get a bot token from [@BotFather](https://t.me/BotFather) on Telegram.
2. Set environment variables:
   ```bash
   # Windows (CMD / PowerShell)
   set TELEGRAM_BOT_TOKEN=your_bot_token_here
   set TELEGRAM_BOT_USERNAME=PRPCEM_PotentialAI_Bot

   # Linux / macOS
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   export TELEGRAM_BOT_USERNAME="PRPCEM_PotentialAI_Bot"
   ```
3. Run the standalone bot runner:
   ```bash
   python platforms/telegram_bot.py
   ```
4. Or set up the Webhook for production:
   ```bash
   curl -F "url=https://your-domain.com/api/telegram/webhook" https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook
   ```

---

## 🧪 Running the Test Suite
To run all 45 automated unit and integration tests:
```bash
pytest tests/ -v
```

---

## 🚀 Free Deployment Guide (e.g., Render)

1. Push your repository to **GitHub**.
2. Log in to [Render](https://render.com/) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the following build and start commands:
   * **Runtime:** `Python`
   * **Build Command:** `pip install -r requirements.txt && python scripts/init_database.py && python scripts/train_model.py`
   * **Start Command:** `gunicorn app:app`
5. Click **Deploy**. Render will automatically detect the port from the environment (`PORT`) and bind to `0.0.0.0`.

---

## 💬 Sample Chatbot Questions to Test

| Topic | Sample Question | Expected Behavior |
| :--- | :--- | :--- |
| **Overview** | *"Tell me about PRPCEM"* | Returns establishment year (2009), trust, NAAC 'A' grade, and DTE Code 1107. |
| **HOD Lookup** | *"Who is the HOD of Computer Engineering?"* | Traverses NetworkX graph and returns **Dr. Manoj M. Andhare** with source link. |
| **Admissions** | *"What is the admission process?"* | Details Maharashtra CAP round procedures, DTE Code 1107, and helpline numbers. |
| **Documents** | *"What documents are required for admission?"* | Lists 14-item required certificate checklist. |
| **Intake** | *"What is the intake of mechanical engineering?"* | Returns approved seat intake (60 seats). |
| **Facilities** | *"Where is the library?"* | Explains Central Library volume collection (35,000+), DELNET, and hours. |
| **Academics** | *"Show me the academic calendar"* | Provides links to Dean Academics portal schedules. |
| **Unrelated Query** | *"What is quantum electrodynamics in astrophysics?"* | Safely triggers **Fallback rule** with confidence &lt; 0.35 and suggests relevant college topics. |

---

## 📜 Limitations & Future Scope
* **Knowledge Boundary:** The assistant only answers questions present within the local PRPCEM knowledge base.
* **Domain Grounding:** Queries unrelated to college administration or academics trigger an informative fallback.
* **Future Scope:** Expanding multi-lingual support (Marathi & Hindi) and voice input/output speech interfaces.

---

## 🎓 Academic Viva Summary
For exam and viva preparation, refer to:
* [`docs/project_report.md`](docs/project_report.md) – Complete 27-section Mini-Project Report.
* [`docs/viva_questions.md`](docs/viva_questions.md) – 35+ Comprehensive Viva Questions and Answers.
