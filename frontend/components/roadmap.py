import streamlit as st
from typing import List, Dict, Any

def render_roadmap(problems: List[Dict[str, Any]], on_select_problem):
    """
    Renders GitHub-style AI Prompt Engineering Roadmap & Problem Directory.
    """
    st.markdown(
        '<div class="github-header">'
        '<div class="github-title">🗺️ AI Prompt Engineering Roadmap</div>'
        '<span class="github-repo-badge">aimap / prompt-challenges</span>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="github-subtitle">'
        'Interactive AI prompt engineering benchmarks on 1B-3B open-source LLMs evaluated against Google, Anthropic, and OpenAI standards.'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Topic Nodes Navigation Cards (GitHub Topics Style)
    st.markdown("### 🏷️ Topic Nodes")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="github-box"><strong>📦 Structured Output</strong><br><small style="color:#8b949e">JSON & XML Constraints</small></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="github-box"><strong>🧠 CoT Reasoning</strong><br><small style="color:#8b949e">&lt;thinking&gt; Scratchpads</small></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="github-box"><strong>🎭 System Persona</strong><br><small style="color:#8b949e">Safety & Role Defense</small></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="github-box"><strong>🎯 Few-Shot Exemplars</strong><br><small style="color:#8b949e">Output Calibration</small></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown(f"### 🟢 Open Benchmarks ({len(problems)})")
    
    for prob in problems:
        diff = prob.get("difficulty", "Easy")
        badge_class = "badge-easy" if diff == "Easy" else ("badge-medium" if diff == "Medium" else "badge-hard")
        
        with st.container():
            st.markdown('<div class="github-box">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3.5, 1.5, 1])
            with c1:
                st.markdown(f"#### 🟢 {prob.get('title')}")
                st.markdown(
                    f"<span class='github-badge {badge_class}'>{diff}</span>"
                    f"<span class='github-badge badge-info'>Node: {prob.get('topic_node')}</span>",
                    unsafe_allow_html=True
                )
                st.markdown(f"<div style='color:#8b949e; margin-top:8px;'>{prob.get('description')}</div>", unsafe_allow_html=True)
                st.caption(f"Target Model: `{prob.get('recommended_model')}`")
            with c2:
                st.markdown("**Category**")
                st.write(prob.get("category"))
            with c3:
                st.markdown("&nbsp;")
                if st.button("Start Challenge ⚡", key=f"btn_{prob.get('id')}"):
                    on_select_problem(prob.get("id"))
            st.markdown('</div>', unsafe_allow_html=True)
