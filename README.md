# 🎯 Prompt Engineering Test

An evaluation platform designed to assess candidate prompt engineering skills against expert standards and guardrails.

🔗 **Live Application**: [https://prompt-engineering-test-nim23jlzuqlqwl9n8lydrb.streamlit.app/](https://prompt-engineering-test-nim23jlzuqlqwl9n8lydrb.streamlit.app/)

---

## ✨ Features

- **Prompt Engineering Test**: Evaluate system and user prompts across real-world engineering scenarios.
- **Diagnostic Quiz**: Multi-select challenges testing prompt structure and guardrail compliance.
- **GitHub Dark Theme**: GitHub Dark UI (`#0d1117`, `#161b22`, `#30363d`).
- **Clean Input Editors**: Empty prompt textareas by default for candidate evaluation.

---

## ⚡ Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/rishabhg8/prompt-engineering-test.git
cd prompt-engineering-test

# Install dependencies and run app
uv sync
uv run streamlit run frontend/app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Testing

Run the unittest suite:

```bash
uv run python -m unittest discover -s tests
```

---

## 📂 Architecture

```
├── app/                  # Backend services and evaluation logic
├── frontend/             # Streamlit app and GitHub Dark CSS theme
│   ├── app.py            # Main entrypoint
│   └── style.css         # GitHub Dark theme stylesheet
├── tests/                # Unittest suite
└── README.md
```
