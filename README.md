# 🎯 Prompt Engineering Test Platform

A modern, minimal candidate evaluation platform for **Prompt Engineering Interviews**, built with Streamlit, FastAPI, and Google's official **5-Step Prompting Framework (`T-C-R-E-I`)**.

---

## 🌟 Key Features

- **🎯 Scenario-Based Prompting Tests**: Real-world AI engineering task scenarios (Customer Support Email, GCP Cloud Architecture Proposal, Zero-Shot SQL JSON Extraction, Medical Triage Guardrails).
- **📊 Google 5-Step Diagnostic Engine**: Automated evaluation against **Task, Context, References, Evaluate, and Iterate** (`T-C-R-E-I`).
- **🧩 Multi-Select Diagnostic Quiz**: Interactive MCQ challenges testing candidates' diagnostic ability to catch flawed or well-crafted prompts.
- **🎨 GitHub Dark Mode Theme**: Sleek, high-contrast dark theme styling (`#0d1117`, `#161b22`, `#30363d`, `#238636`).
- **⚡ Clean Developer UX**: 100% empty candidate input boxes by default with zero placeholder text clutter.

---

## 🚀 Quick Start & Local Running

### Prerequisites
- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) package runner

### 1. Clone & Install
```bash
git clone https://github.com/<your-username>/prompt-engineering-test.git
cd prompt-engineering-test
uv sync
```

### 2. Launch the Application
```bash
uv run streamlit run frontend/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.

### 3. Run Unit Test Suite
```bash
uv run python -m unittest discover -s tests
```

---

## 🏗️ Project Architecture

```
projects/
├── app/
│   ├── models/schemas.py             # Pydantic schemas
│   ├── services/
│   │   ├── google_guardrails.py      # T-C-R-E-I Evaluation Engine
│   │   ├── task_scenarios.py         # Curated AI Engineering Scenarios
│   │   └── mcq_bank.py               # Diagnostic Quiz Questions
│   └── main.py                       # FastAPI API Backend
├── frontend/
│   ├── app.py                        # Streamlit Main App
│   ├── style.css                     # GitHub Dark Theme System
│   └── components/
│       ├── guardrail_checker.py      # Candidate Prompt Test View
│       └── mcq_quiz.py               # Diagnostic Quiz View
├── tests/                            # Comprehensive Unittest Suite
└── README.md
```

---

## ☁️ Deploying on Streamlit Community Cloud

1. Push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub repository.
4. Set **Main file path** to `frontend/app.py`.
5. Click **Deploy**!
