import streamlit as st
from app.services.mcq_bank import get_all_mcqs, get_mcq_by_id

def render_mcq_quiz():
    """
    Renders Diagnostic Quiz with Apple PM minimal aesthetics.
    """
    st.markdown(
        """
        <div class="pm-header">
            <div class="pm-title">Diagnostic Quiz</div>
        </div>
        <div class="pm-subtitle">
            Select all correct statements regarding prompt structure and guardrails.
        </div>
        """,
        unsafe_allow_html=True
    )

    mcqs = get_all_mcqs()
    
    selected_mcq_id = st.selectbox(
        "Select Challenge",
        options=[q.id for q in mcqs],
        format_func=lambda x: f"{get_mcq_by_id(x).title} [{get_mcq_by_id(x).difficulty}]"
    )
    
    q = get_mcq_by_id(selected_mcq_id)
    
    st.markdown(
        f"""
        <div class="pm-card-scenario">
            <h3 style="color:#58a6ff !important; margin-bottom:12px !important;">📋 Scenario: {q.title}</h3>
            <div style="margin-bottom:12px; line-height:1.6;">{q.scenario_description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("**Demo Prompt Under Inspection:**")
    st.code(q.demo_prompt, language="markdown")

    st.markdown("### ❓ Select All Correct Statements:")
    
    user_selections = {}
    for opt in q.options:
        key = f"chk_{q.id}_{opt.id}"
        user_selections[opt.id] = st.checkbox(opt.text, key=key)

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    if st.button("Submit Answer", use_container_width=True):
        selected_ids = [opt_id for opt_id, selected in user_selections.items() if selected]
        correct_ids = [opt.id for opt in q.options if opt.is_correct]

        is_perfect = set(selected_ids) == set(correct_ids)

        if is_perfect:
            st.success("🎉 Correct! You identified all key prompt engineering criteria.")
        else:
            st.warning("⚠️ Review the detailed breakdown below.")

        st.markdown("### 🔍 Option Breakdown")
        for opt in q.options:
            was_selected = user_selections.get(opt.id, False)
            should_be = opt.is_correct
            
            if was_selected == should_be:
                pill_style = "pill-success"
                status_text = "✓ Correct"
            else:
                pill_style = "pill-danger"
                status_text = "✗ Incorrect"
                
            st.markdown(
                f"""
                <div class="pm-card">
                    <strong>{opt.text}</strong><br>
                    <span class="pm-pill {pill_style}" style="margin-top:6px;">{status_text}</span>
                    <span style="font-size:0.85rem; color:#8b949e; margin-left:8px;">{opt.explanation}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
