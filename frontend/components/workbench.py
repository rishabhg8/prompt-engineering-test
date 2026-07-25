import streamlit as st
from typing import Dict, Any, Callable

def render_workbench(problem: Dict[str, Any], on_evaluate: Callable):
    """
    Renders GitHub-style Candidate & Interviewer Workbench.
    """
    st.markdown(
        f'<div class="github-header">'
        f'<div class="github-title">⚡ Challenge: {problem.get("title")}</div>'
        f'<span class="github-badge badge-info">{problem.get("difficulty")}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Problem Description Box (GitHub README / Issue Body style)
    st.markdown('<div class="github-box">', unsafe_allow_html=True)
    st.markdown('<div class="github-box-header">📋 README.md — Challenge Objective & Constraints</div>', unsafe_allow_html=True)
    st.write(problem.get("description"))
    
    st.markdown("**Evaluation Checklist:**")
    for crit in problem.get("evaluation_criteria", []):
        st.markdown(f"- 🟢 `{crit}`")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dual Prompt Editor Split View
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### ⚙️ System Prompt (`system_prompt.txt`)")
        system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.get("current_system_prompt", problem.get("starter_system_prompt", "")),
            height=200,
            help="System instructions, persona definition, and XML format rules."
        )
        
    with col_right:
        st.markdown("### 📝 User Prompt (`user_prompt.txt`)")
        user_prompt = st.text_area(
            "User Prompt",
            value=st.session_state.get("current_user_prompt", problem.get("starter_user_prompt", "")),
            height=200,
            help="Task payload, context data, and few-shot examples."
        )

    # Model & Hyperparameter Settings (GitHub Action Parameters style)
    st.markdown("### 🎛️ Execution Parameters")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        selected_model = st.selectbox(
            "Small LLM Engine",
            options=[
                "meta-llama/llama-3.2-1b-instruct",
                "qwen/qwen-2.5-1.5b-instruct",
                "google/gemma-2-2b-it",
                "deepseek/deepseek-r1-distill-qwen-1.5b"
            ],
            index=0
        )
    with sc2:
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    with sc3:
        top_p = st.slider("Top-P", min_value=0.1, max_value=1.0, value=0.9, step=0.05)

    st.session_state["current_system_prompt"] = system_prompt
    st.session_state["current_user_prompt"] = user_prompt

    st.markdown("---")
    if st.button("🚀 Commit & Run Evaluation", use_container_width=True):
        if not user_prompt.strip():
            st.error("Please enter a User Prompt before running evaluation!")
        else:
            with st.spinner("Analyzing prompt against Google, Anthropic & OpenAI standards..."):
                on_evaluate(
                    problem_id=problem.get("id"),
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    selected_model=selected_model,
                    temperature=temperature,
                    top_p=top_p
                )
