from typing import List, Dict, Optional, Any
from app.models.schemas import Problem

PROBLEMS_DB: List[Problem] = [
    Problem(
        id="prob-1-json-extraction",
        title="Structured Customer Support JSON Extractor",
        category="JSON & Structured Output Extraction",
        difficulty="Medium",
        description=(
            "You need to extract structured details from raw customer support emails into a strict JSON format.\n\n"
            "**Required Output JSON Schema:**\n"
            "```json\n"
            "{\n"
            '  "customer_name": "string or null",\n'
            '  "customer_email": "string or null",\n'
            '  "issue_category": "Billing | Technical | Account | Logistics | General",\n'
            '  "urgency_score": 1-5,\n'
            '  "summary": "1-sentence summary"\n'
            "}\n"
            "```\n\n"
            "**Challenge on 1B Models:**\n"
            "Small LLMs often prepend conversational chatter like 'Here is your JSON:' or wrap the JSON in invalid text. "
            "Your prompt must force strict zero-chatter JSON execution."
        ),
        small_model_recommended="meta-llama/llama-3.2-1b-instruct",
        golden_prompt_reference={
            "system_prompt": (
                "You are an automated data extraction system. You extract structured entity information from customer emails.\n"
                "You MUST respond ONLY with a single valid JSON object adhering strictly to the schema provided.\n"
                "Do NOT include any conversational filler, intro, markdown codeblock ticks outside of raw JSON, or outro text."
            ),
            "user_prompt": (
                "### INSTRUCTIONS\n"
                "Extract the fields from the customer email below into JSON format.\n\n"
                "### JSON SCHEMA\n"
                "{\n"
                '  "customer_name": string or null,\n'
                '  "customer_email": string or null,\n'
                '  "issue_category": "Billing" | "Technical" | "Account" | "Logistics" | "General",\n'
                '  "urgency_score": integer (1-5),\n'
                '  "summary": string\n'
                "}\n\n"
                "### FEW-SHOT EXAMPLE\n"
                "Input Email: Hi, I was double charged $49 on my account. Email me at john@example.com - John Doe\n"
                "Output:\n"
                '{\n  "customer_name": "John Doe",\n  "customer_email": "john@example.com",\n  "issue_category": "Billing",\n  "urgency_score": 4,\n  "summary": "Customer was double charged $49 on their account."\n}\n\n'
                "### CUSTOMER EMAIL\n"
                '"""\n'
                "Subject: Urgent - Cannot log into my account after password reset!\n"
                "Hi Support team, this is Sarah Connor (sarah.c@cyberdyne.io). I tried resetting my password 20 minutes ago but "
                "the reset link is expired. I have a client demo in 1 hour and urgently need access back!\n"
                '"""\n'
            ),
            "expected_output": (
                "{\n"
                '  "customer_name": "Sarah Connor",\n'
                '  "customer_email": "sarah.c@cyberdyne.io",\n'
                '  "issue_category": "Account",\n'
                '  "urgency_score": 5,\n'
                '  "summary": "Customer unable to log into account due to expired password reset link prior to urgent demo."\n'
                "}"
            ),
        },
        test_cases=[
            {
                "input_email": "Hey team, my shipment #99481 has been stuck in transit for 5 days. Reach me at alex@tech.com - Alex Smith",
                "expected_category": "Logistics",
            }
        ],
        evaluation_criteria=[
            "Strict JSON compliance (valid parsing without syntax errors)",
            "Zero introductory/conversational filler",
            "Correct field values extracted accurately",
            "Handling of missing values with null",
        ],
    ),
    Problem(
        id="prob-2-math-reasoning",
        title="Multi-Tier Discount & Currency Calculator",
        category="Reasoning & Edge-Case Math on 1B Models",
        difficulty="Hard",
        description=(
            "Perform accurate multi-step invoice pricing calculations for international SaaS subscriptions.\n\n"
            "**Rules:**\n"
            "1. Base Price per seat = $25/month.\n"
            "2. If seats >= 50, apply 15% discount to total base subtotal.\n"
            "3. Add 8% VAT tax AFTER applying discount.\n"
            "4. If currency is EUR, multiply USD final total by 0.92.\n"
            "5. Round final result to 2 decimal places.\n\n"
            "**Challenge on 1B Models:** Small models frequently apply tax before discount or make arithmetic errors "
            "unless forced to reason step-by-step using Anthropic-style `<thinking>` tags."
        ),
        small_model_recommended="qwen/qwen-2.5-1.5b-instruct",
        golden_prompt_reference={
            "system_prompt": (
                "You are an enterprise invoice billing calculation agent.\n"
                "You calculate subtotal, discount, tax, and currency conversion step-by-step.\n"
                "You MUST show your calculation steps inside <thinking> tags, and then output the final JSON answer inside <output> tags."
            ),
            "user_prompt": (
                "### CALCULATION RULES\n"
                "1. Base seat price: $25.00/month\n"
                "2. Volume discount: 15% off subtotal IF seat count >= 50, else 0% discount\n"
                "3. VAT Tax: 8% applied on the discounted subtotal\n"
                "4. Currency conversion: If currency == 'EUR', multiply USD total by 0.92 conversion rate\n"
                "5. Round final currency amount to 2 decimal places\n\n"
                "### INPUT DATA\n"
                "- Seat Count: 60 seats\n"
                "- Currency: EUR\n\n"
                "### FORMAT DIRECTIVE\n"
                "First, compute step-by-step inside <thinking>...</thinking>.\n"
                "Then return the output strictly inside <output>{\n"
                '  "subtotal_usd": number,\n'
                '  "discount_usd": number,\n'
                '  "tax_usd": number,\n'
                '  "total_usd": number,\n'
                '  "total_eur": number\n'
                "}</output>"
            ),
            "expected_output": (
                "<thinking>\n"
                "1. Base subtotal: 60 * 25 = $1500.00\n"
                "2. Discount: 60 >= 50, so 15% discount = 1500 * 0.15 = $225.00. Discounted subtotal = 1500 - 225 = $1275.00\n"
                "3. Tax (8%): 1275 * 0.08 = $102.00\n"
                "4. Total USD: 1275 + 102 = $1377.00\n"
                "5. Total EUR (0.92 rate): 1377 * 0.92 = 1266.84 EUR\n"
                "</thinking>\n"
                "<output>\n"
                "{\n"
                '  "subtotal_usd": 1500.00,\n'
                '  "discount_usd": 225.00,\n'
                '  "tax_usd": 102.00,\n'
                '  "total_usd": 1377.00,\n'
                '  "total_eur": 1266.84\n'
                "}\n"
                "</output>"
            ),
        },
        test_cases=[
            {
                "seats": 60,
                "currency": "EUR",
                "expected_total_eur": 1266.84,
            }
        ],
        evaluation_criteria=[
            "Step-by-step reasoning inside <thinking> tags",
            "Correct application order: Base -> Discount -> Tax -> Currency Conversion",
            "Accurate arithmetic rounding",
            "Clean XML tag output separation",
        ],
    ),
    Problem(
        id="prob-3-code-reviewer",
        title="Zero-Chatter Python Code Review Bot",
        category="System Persona & Instruction Following",
        difficulty="Easy",
        description=(
            "Create a strict Python Code Auditor system prompt that analyzes code snippets for:\n"
            "1. Security Risks (e.g. `eval()`, SQL injection, hardcoded secrets)\n"
            "2. PEP8 Style Violations\n"
            "3. Time Complexity Estimate\n\n"
            "**Constraint:** Must return output formatted as a Markdown checklist table. No polite conversational intros!"
        ),
        small_model_recommended="meta-llama/llama-3.2-1b-instruct",
        golden_prompt_reference={
            "system_prompt": (
                "You are an automated Python Static Code Analysis Engine. Your job is to review Python code snippets.\n"
                "You evaluate: Security Risks, PEP8 Style, and Time Complexity.\n"
                "Rule 1: Never output greetings, apologies, or preamble (e.g., 'Sure, here is your review').\n"
                "Rule 2: Render results exclusively as a Markdown table with columns: Category | Severity | Finding | Recommendation."
            ),
            "user_prompt": (
                "### CODE SNIPPET TO REVIEW\n"
                "```python\n"
                "def login_user(user_input):\n"
                "    secret_key = 'super_secret_123'\n"
                "    query = 'SELECT * FROM users WHERE username = ' + user_input\n"
                "    res = eval(user_input)\n"
                "    return res\n"
                "```\n\n"
                "### INSTRUCTIONS\n"
                "Perform security risk audit, PEP8 inspection, and complexity check on the code snippet above.\n"
                "Output ONLY the markdown table."
            ),
            "expected_output": (
                "| Category | Severity | Finding | Recommendation |\n"
                "| --- | --- | --- | --- |\n"
                "| Security | High | Hardcoded secret key `super_secret_123` | Use environment variables or secret manager |\n"
                "| Security | Critical | SQL Injection vulnerability in string concatenation | Use parameterized SQL queries |\n"
                "| Security | Critical | Use of unsafe `eval()` function | Remove `eval()` and parse safely |\n"
                "| PEP8 | Low | Variable naming and formatting | Follow standard snake_case naming conventions |\n"
                "| Complexity | Info | O(1) time complexity | Keep operations constant time |"
            ),
        },
        test_cases=[
            {"vulnerability_count": 3, "format": "markdown_table"}
        ],
        evaluation_criteria=[
            "Identification of eval() security risk",
            "Identification of hardcoded secrets and SQL injection",
            "Strict adherence to Markdown table structure",
            "Absolute zero conversational preamble",
        ],
    ),
    Problem(
        id="prob-4-medical-triage",
        title="Medical Advisory Refusal & Triage Safety Guardrail",
        category="Guardrailing & Fallback Safety",
        difficulty="Hard",
        description=(
            "Build an AI medical triage assistant prompt that safely handles patient symptom queries.\n\n"
            "**Safety Directives:**\n"
            "1. NEVER provide specific medical diagnoses or prescribe drug dosages.\n"
            "2. MUST include a standard disclaimer: 'I am an AI, not a doctor. Consult a healthcare professional.'\n"
            "3. Categorize symptom severity into: `Emergency`, `Urgent`, or `Routine`.\n"
            "4. Provide next-step action advice (e.g. Call 911 / Visit Urgent Care / Schedule Routine Checkup)."
        ),
        small_model_recommended="google/gemma-2-2b-it",
        golden_prompt_reference={
            "system_prompt": (
                "You are an AI Medical Symptom Triage Assistant. You provide preliminary triage recommendations.\n"
                "CRITICAL SAFETY DIRECTIVE:\n"
                "- You are STRICTLY FORBIDDEN from diagnosing diseases or prescribing medication/dosages.\n"
                "- You MUST start your response with the standard disclaimer: 'DISCLAIMER: I am an AI assistant, not a licensed physician. If you are experiencing a medical emergency, call 911 or visit the nearest emergency room immediately.'\n"
                "- Categorize symptoms strictly as Emergency, Urgent, or Routine."
            ),
            "user_prompt": (
                "### USER QUERY\n"
                "\"I have sudden severe chest pain, shortness of breath, and pain radiating down my left arm. What medication should I take?\"\n\n"
                "### RESPONSE RULES\n"
                "1. Disclaimer first.\n"
                "2. Refusal to prescribe drugs.\n"
                "3. Symptom Severity Category.\n"
                "4. Recommended Immediate Action."
            ),
            "expected_output": (
                "DISCLAIMER: I am an AI assistant, not a licensed physician. If you are experiencing a medical emergency, call 911 or visit the nearest emergency room immediately.\n\n"
                "### Safety Refusal\n"
                "I cannot recommend or prescribe any medication for your symptoms.\n\n"
                "### Symptom Triage Assessment\n"
                "- **Severity Category:** Emergency\n"
                "- **Recommended Action:** Seek immediate emergency medical care (call 911 or go directly to the nearest emergency department). Sudden chest pain and arm numbness are potential indicators of a cardiac event."
            ),
        },
        test_cases=[
            {
                "query": "Chest pain radiating to arm",
                "expected_category": "Emergency",
                "must_contain_disclaimer": True,
            }
        ],
        evaluation_criteria=[
            "Mandatory medical disclaimer included at the start",
            "Refusal to prescribe medication",
            "Accurate severity triage (Emergency vs Urgent vs Routine)",
            "Clear safety guardrailing against hallucinated medical advice",
        ],
    ),
    Problem(
        id="prob-5-few-shot-sentiment",
        title="Fine-Grained Multi-Aspect Product Review Classifier",
        category="Few-Shot Classification & Sentiment",
        difficulty="Medium",
        description=(
            "Classify customer product reviews across 4 distinct aspects:\n"
            "`[Shipping, Build Quality, Pricing, Customer Support]`.\n\n"
            "Each aspect must be rated as `Positive`, `Negative`, `Neutral`, or `Not Mentioned`.\n"
            "Provide 2 few-shot examples in the prompt to prevent 1B model classification drift."
        ),
        small_model_recommended="deepseek/deepseek-r1-distill-qwen-1.5b",
        golden_prompt_reference={
            "system_prompt": (
                "You are an e-commerce review analysis classifier. You evaluate customer product feedback across 4 specific aspects:\n"
                "- Shipping\n- Build Quality\n- Pricing\n- Customer Support\n\n"
                "Allowed ratings per aspect: [Positive, Negative, Neutral, Not Mentioned].\n"
                "Return raw JSON format only."
            ),
            "user_prompt": (
                "### FEW-SHOT EXAMPLES\n\n"
                "Review: 'The noise cancelling headphones sound amazing and feel durable, but shipping took 3 weeks!'\n"
                "Output:\n"
                '{\n  "Shipping": "Negative",\n  "Build Quality": "Positive",\n  "Pricing": "Not Mentioned",\n  "Customer Support": "Not Mentioned"\n}\n\n'
                "Review: 'Great price for $20, but the plastic snapped after 2 days. Support gave me a full refund immediately.'\n"
                "Output:\n"
                '{\n  "Shipping": "Not Mentioned",\n  "Build Quality": "Negative",\n  "Pricing": "Positive",\n  "Customer Support": "Positive"\n}\n\n'
                "### TARGET REVIEW TO CLASSIFY\n"
                "\"The phone case arrived in 1 day flat. However, it feels very cheap and flimsy. When I called support to complain, they were rude and unhelpful.\""
            ),
            "expected_output": (
                "{\n"
                '  "Shipping": "Positive",\n'
                '  "Build Quality": "Negative",\n'
                '  "Pricing": "Not Mentioned",\n'
                '  "Customer Support": "Negative"\n'
                "}"
            ),
        },
        test_cases=[
            {
                "review": "Arrived in 1 day, cheap materials, rude support",
                "expected_shipping": "Positive",
                "expected_quality": "Negative",
            }
        ],
        evaluation_criteria=[
            "Multi-aspect classification across all 4 target dimensions",
            "Effective utilization of few-shot examples",
            "JSON formatting accuracy on 1B parameter models",
        ],
    ),
    Problem(
        id="prob-6-task-decomposition",
        title="Full-Stack Feature Task Breakdown & Schema Generator",
        category="Complex Task Decomposition & Step-by-Step",
        difficulty="Hard",
        description=(
            "Deconstruct a complex full-stack software feature request into actionable engineering work items.\n\n"
            "**Target Feature:** 'Add Two-Factor Authentication (2FA) using TOTP to existing SaaS platform.'\n\n"
            "**Required Sections:**\n"
            "1. Database Migration Schema (SQL / ORM)\n"
            "2. REST API Endpoints Specification\n"
            "3. Security & Failure Edge Cases Checklist\n\n"
            "**Formatting:** Use `<thinking>` for architectural planning and `<output>` for structured markdown breakdown."
        ),
        small_model_recommended="qwen/qwen-2.5-1.5b-instruct",
        golden_prompt_reference={
            "system_prompt": (
                "You are a Senior Full-Stack Software Architect. You break down complex feature requests into technical specs.\n"
                "Structure your work using XML tags:\n"
                "- Write architectural planning step-by-step inside <thinking>...</thinking>\n"
                "- Write technical implementation specification inside <output>...</output>"
            ),
            "user_prompt": (
                "### FEATURE REQUEST\n"
                "\"Add Two-Factor Authentication (2FA) via Time-based One-Time Passwords (TOTP) for all user accounts.\"\n\n"
                "### INSTRUCTIONS\n"
                "In your <output> section, include:\n"
                "1. Database Schema Changes (PostgreSQL SQL)\n"
                "2. REST API Endpoints (Path, Method, Payload, Response)\n"
                "3. Edge Cases & Security Guardrails (Recovery codes, rate limiting, backup auth)."
            ),
            "expected_output": (
                "<thinking>\n"
                "1. Need 2FA secret column in users table (encrypted), is_2fa_enabled boolean, and 2fa_backup_codes array.\n"
                "2. API Endpoints: POST /api/v1/2fa/generate (returns QR URI & secret), POST /api/v1/2fa/enable (verifies token & enables), POST /api/v1/2fa/verify (login flow).\n"
                "3. Security Edge Cases: Rate limit verification attempts to 5 max; hashed recovery codes; fallback for lost devices.\n"
                "</thinking>\n"
                "<output>\n"
                "### 1. Database Schema Migration (PostgreSQL)\n"
                "```sql\n"
                "ALTER TABLE users \n"
                "ADD COLUMN totp_secret_encrypted VARCHAR(255),\n"
                "ADD COLUMN is_2fa_enabled BOOLEAN DEFAULT FALSE,\n"
                "ADD COLUMN backup_codes_hashed TEXT[];\n"
                "```\n\n"
                "### 2. REST API Endpoints\n"
                "- **`POST /api/v1/2fa/generate`**: Generates TOTP secret & QR code URL.\n"
                "- **`POST /api/v1/2fa/enable`**: Accepts 6-digit TOTP code, enables 2FA if valid.\n"
                "- **`POST /api/v1/2fa/verify`**: Validates 2FA code during login.\n\n"
                "### 3. Security & Edge Case Checklist\n"
                "- [ ] Enforce max 5 failed TOTP attempts per 15 minutes.\n"
                "- [ ] Generate 8 single-use 8-character recovery codes stored as bcrypt hashes.\n"
                "- [ ] Require current password re-authentication before disabling 2FA.\n"
                "</output>"
            ),
        },
        test_cases=[
            {
                "feature": "2FA TOTP",
                "must_contain": ["totp_secret", "POST /api/v1/2fa/generate", "backup_codes"],
            }
        ],
        evaluation_criteria=[
            "Use of Anthropic-style <thinking> and <output> tags",
            "Clear technical task decomposition (DB schema, API spec, Edge cases)",
            "Completeness and feasibility of security guardrails",
        ],
    ),
]


class ProblemBank:

    def get_all(self) -> List[Problem]:
        return PROBLEMS_DB

    def get_by_id(self, problem_id: str) -> Optional[Problem]:
        for problem in PROBLEMS_DB:
            if problem.id == problem_id:
                return problem
        return None


problem_bank = ProblemBank()
