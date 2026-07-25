import streamlit as st
import sys
import os

# Ensure root workspace directory is on sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.services.google_guardrails import GoogleGuardrailsEvaluator, GooglePromptAnalysis

try:
    from app.services.task_scenarios import get_all_scenarios, get_scenario_by_id
except ImportError:
    from app.services.task_scenarios import TASK_SCENARIOS, task_scenario_bank
    def get_all_scenarios():
        return TASK_SCENARIOS
    def get_scenario_by_id(sid):
        scen = task_scenario_bank.get_by_id(sid)
        return scen if scen else TASK_SCENARIOS[0]

def render_guardrail_checker():
    """
    Renders Prompt Engineering Test main page with Apple PM minimal aesthetics.
    """
    st.markdown(
        """
        <div class="pm-header">
            <div class="pm-title">Prompt Engineering Test</div>
        </div>
        <div class="pm-subtitle">
            Evaluate candidate prompts against expert engineering standards.
        </div>
        """,
        unsafe_allow_html=True
    )

    scenarios = get_all_scenarios()
    
    # 1. TASK SCENARIO SELECTION DROPDOWN
    selected_scen_id = st.selectbox(
        "Select Scenario",
        options=[s.id for s in scenarios],
        format_func=lambda x: f"{get_scenario_by_id(x).title} [{get_scenario_by_id(x).category} • {get_scenario_by_id(x).difficulty}]"
    )
    
    scen = get_scenario_by_id(selected_scen_id)

    # 2. PROMINENT TASK SCENARIO CARD FOR CANDIDATE REFERENCE
    st.markdown(
        f"""
        <div class="pm-card-scenario">
            <h3 style="color:#58a6ff !important; margin-bottom:12px !important;">📋 Scenario Brief: {scen.title}</h3>
            <div style="margin-bottom:8px; line-height:1.6;"><strong>Objective:</strong> {scen.objective}</div>
            <div style="margin-bottom:8px; line-height:1.6;"><strong>Context:</strong> {scen.background_context}</div>
            <div style="margin-bottom:8px; line-height:1.6;"><strong>Payload:</strong> <code>{scen.input_data_payload}</code></div>
            <div style="line-height:1.6;"><strong>Format:</strong> <code>{scen.target_format}</code></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. CANDIDATE PROMPT EDITORS (COMPLETELY EMPTY BY DEFAULT)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**⚙️ System Prompt**")
        system_prompt = st.text_area(
            "System Prompt Area",
            value=st.session_state.get(f"sys_{scen.id}", ""),
            height=220,
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("**📝 User Prompt**")
        user_prompt = st.text_area(
            "User Prompt Area",
            value=st.session_state.get(f"user_{scen.id}", ""),
            height=220,
            label_visibility="collapsed"
        )

    st.session_state[f"sys_{scen.id}"] = system_prompt
    st.session_state[f"user_{scen.id}"] = user_prompt

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    if st.button("Run Diagnostic", use_container_width=True):
        if not user_prompt.strip():
            st.error("Please enter a User Prompt to evaluate!")
        else:
            analysis: GooglePromptAnalysis = GoogleGuardrailsEvaluator.analyze(system_prompt, user_prompt)
            st.session_state["analysis_result"] = analysis

    # 4. DIAGNOSTIC RESULTS DISPLAY
    analysis = st.session_state.get("analysis_result")
    if analysis:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📊 Diagnostic Scorecard")
        
        c_score, c_passed, c_missing = st.columns([1, 1.5, 1.5])
        with c_score:
            color = "#3fb950" if analysis.overall_score >= 80 else ("#d29922" if analysis.overall_score >= 50 else "#f85149")
            st.markdown(
                f"""
                <div class="pm-score-card">
                    <div style="color:#8b949e; font-size:0.85rem; font-weight:500;">Overall Score</div>
                    <div class="pm-score-val" style="color:{color};">{analysis.overall_score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_passed:
            st.markdown("#### ✅ Passed Criteria")
            for step in analysis.passed_steps:
                st.markdown(f'<span class="pm-pill pill-success">✓ {step}</span>', unsafe_allow_html=True)
        with c_missing:
            st.markdown("#### ⚠️ Missing Criteria")
            for step in analysis.missing_steps:
                st.markdown(f'<span class="pm-pill pill-danger">✗ {step}</span>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Evaluation")
        
        for check in analysis.checks:
            icon = "✅" if check.passed else "❌"
            pill_style = "pill-success" if check.passed else "pill-danger"
            st.markdown(
                f"""
                <div class="pm-card">
                    <span class="pm-pill {pill_style}">{icon} {check.step_name}: {check.element}</span>
                    <div style="margin-top:10px; color:#c9d1d9; font-size:0.9rem;">{check.feedback}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if analysis.actionable_suggestions:
            st.markdown("### 💡 Suggestions")
            suggs_html = "".join([f"<div style='margin-bottom:6px;'>👉 {s}</div>" for s in analysis.actionable_suggestions])
            st.markdown(
                f"""
                <div class="pm-card" style="border-left: 4px solid #d29922;">
                    {suggs_html}
                </div>
                """,
                unsafe_allow_html=True
            )
