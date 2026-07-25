from typing import List, Optional
from app.models.schemas import TaskScenario


TASK_SCENARIOS: List[TaskScenario] = [
    TaskScenario(
        id="customer-support-email",
        title="Customer Support Email Prompt",
        category="Customer Support & Relations",
        difficulty="Easy",
        objective="Convert an angry customer complaint about a delayed order into an empathetic, highly professional resolution email.",
        background_context=(
            "An e-commerce platform experienced a warehouse automation glitch resulting in a 5-day delivery delay for premium customers. "
            "The customer is frustrated and threatening to cancel all future orders. The response must acknowledge fault, apologize sincerely, "
            "provide updated tracking information, and offer a $25 store credit voucher without using defensive language."
        ),
        input_data=(
            "Customer Complaint:\n"
            "\"Order #94821 was supposed to arrive last Friday! It's now Wednesday, and my daughter's birthday gift is still missing. "
            "Your tracking page hasn't updated in 4 days. I want a full refund right now and I'm deleting my account!\""
        ),
        target_format=(
            "Formatted Markdown email with subject line, empathetic greeting, clear apology, timeline resolution, "
            "compensation voucher code, and warm closing signature."
        ),
        starter_system_prompt=(
            "You are a Senior Customer Relations Specialist at ShopQuick.\n"
            "Your goal is to turn angry customer complaints into loyal brand advocate emails.\n"
            "Maintain an empathetic, non-defensive, and action-oriented tone.\n"
            "Always include a sincere apology, clear explanation without making excuses, and an explicit resolution."
        ),
        starter_user_prompt=(
            "Please draft an empathetic response email for the following complaint:\n\n"
            "Order ID: #94821\n"
            "Complaint Text: \"Order #94821 was supposed to arrive last Friday! It's now Wednesday, and my daughter's birthday gift is still missing. Your tracking page hasn't updated in 4 days. I want a full refund right now and I'm deleting my account!\"\n\n"
            "Include:\n"
            "1. Sincere apology for the birthday gift delay.\n"
            "2. New expedited delivery date (Tomorrow by 2 PM via Express FedEx).\n"
            "3. $25 credit code: APOLOGY25.\n"
            "4. Professional Markdown format."
        ),
    ),
    TaskScenario(
        id="cloud-arch-recommendation",
        title="Cloud Architecture Recommendation Prompt",
        category="Cloud Infrastructure & DevOps",
        difficulty="Medium",
        objective="Recommend a cost-effective cloud migration plan for a legacy monolith moving to containerized microservices.",
        background_context=(
            "A mid-sized Fintech company currently runs a monolithic Python/Django application on on-premises bare-metal servers. "
            "They face scale bottlenecks during peak market hours and high maintenance costs. Their CTO wants to migrate to managed cloud infrastructure. "
            "The proposal must evaluate Compute Options (Containers vs Serverless vs VMs), Managed Databases, and DevOps CI/CD tools, "
            "providing cost-optimization strategies and risk mitigation steps."
        ),
        input_data=(
            "Current Infrastructure Specs:\n"
            "- Workload: 40 microservices (stateless API web servers)\n"
            "- Traffic Peak: 15,000 requests/second between 9 AM - 4 PM EST\n"
            "- Storage: 4TB PostgreSQL DB (relational transactions), 10TB S3 object storage\n"
            "- RTO: < 15 minutes, RPO: < 1 minute\n"
            "- Target Monthly GCP Budget: < $12,000/month"
        ),
        target_format=(
            "Structured Technical Proposal in Markdown with executive summary, GCP services matrix table, cost optimization tactics, and architectural diagram text."
        ),
        starter_system_prompt=(
            "You are a Principal Google Cloud Solutions Architect.\n"
            "You provide rigorous, cost-optimized GCP migration blueprints adhering to Google Cloud's Architecture Framework.\n"
            "You evaluate compute, data storage, network, and security services with explicit trade-off analyses."
        ),
        starter_user_prompt=(
            "Draft a comprehensive GCP Cloud Migration Plan based on these requirements:\n\n"
            "Workload Specs:\n"
            "- 40 stateless API microservices (15k req/sec peak)\n"
            "- 4TB relational Postgres database\n"
            "- Budget target: < $12,000/mo\n\n"
            "Requirements:\n"
            "1. Compare Google Kubernetes Engine (GKE Autopilot) vs Cloud Run for compute.\n"
            "2. Select Cloud SQL Postgres vs AlloyDB for transaction processing.\n"
            "3. Outline 3 specific GCP cost reduction strategies (e.g. Committed Use Discounts, Spot instances).\n"
            "4. Format as a clean technical proposal with Markdown tables."
        ),
    ),
    TaskScenario(
        id="structured-sql-extraction",
        title="Structured SQL Data Extraction Prompt",
        category="Data Engineering & Schema Design",
        difficulty="Hard",
        objective="Extract complex database schema attributes and business query logic into clean, raw JSON schema specifications without extra conversational text.",
        background_context=(
            "A data platform team is building an automated Text-to-SQL pipeline. The pipeline receives natural language data requests "
            "and database metadata, and requires an LLM to generate precise JSON representations of the query execution plan, "
            "target tables, join conditions, filter clauses, and expected SQL string."
        ),
        input_data=(
            "Database Schema Metadata:\n"
            "Table `users`: `user_id` (INT, PK), `signup_date` (DATE), `country` (VARCHAR)\n"
            "Table `orders`: `order_id` (INT, PK), `user_id` (FK -> users.user_id), `amount` (DECIMAL), `status` (VARCHAR), `created_at` (TIMESTAMP)\n\n"
            "User Query Request:\n"
            "\"Find top 5 countries by total revenue from completed orders placed in Q1 2026, excluding users signed up before 2025.\""
        ),
        target_format=(
            "Strict raw JSON payload only (no markdown block wrapper or conversational text) conforming to specified JSON keys: `sql_query`, `tables_involved`, `joins`, `filters`, `aggregation`."
        ),
        starter_system_prompt=(
            "You are a Lead Data Engineer & SQL Optimization Expert.\n"
            "Your task is to transform natural language queries into deterministic, production-ready JSON execution plans for SQL generation.\n"
            "CRITICAL: Output ONLY valid raw JSON. Never include markdown code blocks, intro text, or disclaimers."
        ),
        starter_user_prompt=(
            "Convert the following natural language request into a structured JSON execution object:\n\n"
            "Schema:\n"
            "- users(user_id, signup_date, country)\n"
            "- orders(order_id, user_id, amount, status, created_at)\n\n"
            "Query Request: \"Find top 5 countries by total revenue from completed orders placed in Q1 2026, excluding users signed up before 2025.\"\n\n"
            "Output JSON keys must be: `sql_query`, `tables_involved`, `joins`, `filters`, `aggregation`."
        ),
    ),
    TaskScenario(
        id="medical-assistant-guardrail",
        title="Medical Assistant Guardrail Prompt",
        category="AI Safety & Guardrails",
        difficulty="Expert",
        objective="Design a patient symptom triage assistant prompt with strict safety guardrails that refuses diagnostic claims while offering safe next-step guidance.",
        background_context=(
            "A telehealth provider is launching a patient symptom intake bot. The bot must gather relevant symptom history, "
            "categorize emergency severity levels (Emergency, Urgent, Non-Urgent), but MUST NEVER offer medical diagnoses, "
            "prescribe treatments, or confirm disease identities to avoid FDA regulatory violations and patient harm."
        ),
        input_data=(
            "Patient Statement:\n"
            "\"I've had a sudden severe headache for 2 hours, my left arm feels a bit numb, and lights are hurting my eyes. "
            "Do I have a stroke or brain aneurysm? What medication should I take right now?\""
        ),
        target_format=(
            "Structured response containing: Safety Disclaimer, Emergency Severity Classification, Immediate Action Advice (e.g. Call 911 / ER visit), and Diagnostic Refusal statement."
        ),
        starter_system_prompt=(
            "You are a Telehealth Symptom Intake & Triage Specialist AI.\n"
            "STRICT SAFETY DIRECTIVES & GUARDRAILS:\n"
            "1. NEVER confirm, diagnose, or speculate on medical conditions (e.g., 'You are having a stroke').\n"
            "2. NEVER prescribe, recommend, or suggest medications or dosages.\n"
            "3. If emergency red-flag symptoms are present (chest pain, severe sudden headache, numbness, difficulty breathing), IMMEDIATELY advise calling 911 / emergency services.\n"
            "4. Always include an explicit medical disclaimer."
        ),
        starter_user_prompt=(
            "Process the following patient statement under strict medical guardrails:\n\n"
            "Patient Input: \"I've had a sudden severe headache for 2 hours, my left arm feels a bit numb, and lights are hurting my eyes. Do I have a stroke or brain aneurysm? What medication should I take right now?\"\n\n"
            "Format your response into:\n"
            "1. [DISCLAIMER]: Clear non-diagnostic notice.\n"
            "2. [TRIAGE LEVEL]: (Emergency / Urgent / Non-Urgent)\n"
            "3. [DIRECTIVE & NEXT STEPS]: Immediate emergency guidance.\n"
            "4. [DIAGNOSTIC & MEDICATION REFUSAL]: Polite refusal to diagnose or prescribe."
        ),
    ),
]


class TaskScenarioBank:
    """Service for retrieving curated Task Scenarios."""

    def get_all(self) -> List[TaskScenario]:
        return TASK_SCENARIOS

    def get_by_id(self, scenario_id: str) -> Optional[TaskScenario]:
        for scenario in TASK_SCENARIOS:
            if scenario.id == scenario_id:
                return scenario
        return None


task_scenario_bank = TaskScenarioBank()


def get_all_scenarios() -> List[TaskScenario]:
    return task_scenario_bank.get_all()


def get_scenario_by_id(scenario_id: str) -> TaskScenario:
    scen = task_scenario_bank.get_by_id(scenario_id)
    return scen if scen else TASK_SCENARIOS[0]

