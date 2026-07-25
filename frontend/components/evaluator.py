import streamlit as st
from typing import Dict, Any

def render_evaluation_report(report: Dict[str, Any]):
    """
    Renders GitHub Actions-style Evaluation Report.
    """
    st.markdown(
        '<div class="github-header">'
        '<div class="github-title">📊 Evaluation Report</div>'
        '<span class="github-badge badge-success">Checks Passed</span>'
        '</div>',
        unsafe_allow_html=True
    )
    
    score = int(report.get("overall_score", 0))
    exec_time = report.get("execution_time_ms", 0.0)
    
    # GitHub Big Metric & Category Scores
    sc1, sc2 = st.columns([1, 2])
    with sc1:
        st.markdown(
            f'<div class="github-score-box">'
            f'<div style="color:#8b949e; font-size:0.9rem;">Overall Prompt Score</div>'
            f'<div class="github-score-val">{score}%</div>'
            f'<div style="color:#8b949e; font-size:0.8rem; margin-top:6px;">⏱️ Latency: {exec_time} ms</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with sc2:
        st.markdown("### Category Score Metrics")
        for cat_name, cat_score in report.get("category_scores", {}).items():
            st.write(f"**{cat_name}** ({cat_score}%)")
            st.progress(float(cat_score) / 100.0)

    st.markdown("---")
    
    # GitHub Action Check Runs
    st.markdown("### ✅ Golden Standard Check Runs")
    checks = report.get("standard_checks", [])
    
    col_g, col_a, col_o = st.columns(3)
    
    with col_g:
        st.markdown("#### 🔵 Google Standards")
        google_checks = [c for c in checks if "Google" in c.get("standard_name", "")]
        for c in google_checks:
            passed = c.get("passed", False)
            icon = "✅" if passed else "❌"
            badge = "badge-success" if passed else "badge-danger"
            st.markdown(
                f'<div class="github-box">'
                f'<span class="github-badge {badge}">{icon} {c.get("criterion")}</span>'
                f'<div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">{c.get("feedback")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
    with col_a:
        st.markdown("#### 🟠 Anthropic Standards")
        anthropic_checks = [c for c in checks if "Anthropic" in c.get("standard_name", "")]
        for c in anthropic_checks:
            passed = c.get("passed", False)
            icon = "✅" if passed else "❌"
            badge = "badge-success" if passed else "badge-danger"
            st.markdown(
                f'<div class="github-box">'
                f'<span class="github-badge {badge}">{icon} {c.get("criterion")}</span>'
                f'<div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">{c.get("feedback")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with col_o:
        st.markdown("#### 🟢 OpenAI Standards")
        openai_checks = [c for c in checks if "OpenAI" in c.get("standard_name", "")]
        for c in openai_checks:
            passed = c.get("passed", False)
            icon = "✅" if passed else "❌"
            badge = "badge-success" if passed else "badge-danger"
            st.markdown(
                f'<div class="github-box">'
                f'<span class="github-badge {badge}">{icon} {c.get("criterion")}</span>'
                f'<div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">{c.get("feedback")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Actionable Suggestions Box
    suggestions = report.get("actionable_suggestions", [])
    if suggestions:
        st.markdown("### 💡 Recommended Fixes for 1B Models")
        st.markdown('<div class="github-box" style="border-left: 4px solid #d29922;">', unsafe_allow_html=True)
        for sugg in suggestions:
            st.markdown(f"👉 {sugg}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Side-by-Side Output Comparison (GitHub Diff Style)
    st.markdown("### 🤖 Output Comparison")
    oc1, oc2 = st.columns(2)
    
    with oc1:
        st.markdown("#### `small_model_output.json`")
        st.code(report.get("small_model_output", ""), language="json")
        
    with oc2:
        st.markdown("#### `golden_reference.json`")
        st.code(report.get("golden_output", ""), language="json")
