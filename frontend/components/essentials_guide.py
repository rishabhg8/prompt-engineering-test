import streamlit as st

def render_essentials_guide():
    """
    Renders Google Prompting Essentials Cheat Sheet based on official takeaway guide.
    """
    st.markdown(
        '<div class="apple-header">'
        '<div class="apple-title-group">'
        '<div class="apple-title">📖 Google Prompting Essentials Cheat Sheet</div>'
        '<div class="apple-subtitle">Master Google\'s official <strong>T-C-R-E-I Framework</strong>, AI Agent Persona Design, and Advanced Iteration Tactics.</div>'
        '</div>'
        '<span class="pill-badge pill-green">Official Google Framework Reference</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🌟 The 5-Step Prompting Framework (`T-C-R-E-I`)")
    st.caption("Thoughtfully Create Really Excellent Inputs")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(
            '<div class="framework-step-card">'
            '<div class="framework-step-title">📋 Task</div>'
            '<span class="pill-badge pill-blue">Step 1</span>'
            '<div class="framework-step-desc">Define the exact goal, assign a persona (System Prompt), and specify the output structure (JSON, Markdown, tables).</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            '<div class="framework-step-card">'
            '<div class="framework-step-title">📄 Context</div>'
            '<span class="pill-badge pill-purple">Step 2</span>'
            '<div class="framework-step-desc">Provide detailed scenario background, target audience, business constraints, and environment parameters.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            '<div class="framework-step-card">'
            '<div class="framework-step-title">📚 References</div>'
            '<span class="pill-badge pill-green">Step 3</span>'
            '<div class="framework-step-desc">Include concrete few-shot examples (Input -> Output pairs), reference documents, or sample schema templates.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            '<div class="framework-step-card">'
            '<div class="framework-step-title">📊 Evaluate</div>'
            '<span class="pill-badge pill-amber">Step 4</span>'
            '<div class="framework-step-desc">Assess generated outputs against acceptance criteria, tone rules, formatting limits, and factual accuracy.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with c5:
        st.markdown(
            '<div class="framework-step-card">'
            '<div class="framework-step-title">🔄 Iterate</div>'
            '<span class="pill-badge pill-red">Step 5</span>'
            '<div class="framework-step-desc">Refine prompts through sub-prompts, negative constraints, Chain-of-Thought (CoT), or prompt chaining.</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 🤖 AI Agent Persona & Workflow Design")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            '<div class="apple-card">'
            '<div class="apple-card-header">5 Steps to Build an AI Agent</div>'
            '<ol style="color:#c9d1d9; line-height:1.8; margin-left:16px;">'
            '<li><strong>Assign Persona:</strong> Define specialized role & expertise level in System Prompt.</li>'
            '<li><strong>Provide Scenario Context:</strong> Supply background, domain rules, and dataset context.</li>'
            '<li><strong>Specify Interaction Style:</strong> Enforce tone, output schema, and behavioral boundaries.</li>'
            '<li><strong>Provide Stop Phrase:</strong> Define clear signal to terminate multi-turn interactions.</li>'
            '<li><strong>Request Takeaways:</strong> Ask model for summary recap or action item extraction upon completion.</li>'
            '</ol>'
            '</div>',
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            '<div class="apple-card">'
            '<div class="apple-card-header">💡 Agent System Prompt Template</div>'
            '```markdown\n'
            'You are a [Expert Persona].\n'
            'Your objective is to [Goal].\n\n'
            'Context: [Background & Data].\n'
            'Constraints:\n'
            '- Do NOT [Negative Constraint]\n'
            '- Output format MUST be [Schema]\n'
            '- Think step-by-step before answering.'
            '```'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 🔄 Iteration & Chain-of-Thought (CoT) Tactics")
    
    c_t1, c_t2, c_t3 = st.columns(3)
    with c_t1:
        st.markdown(
            '<div class="apple-card">'
            '<div class="apple-card-header">🔗 Prompt Chaining</div>'
            '<p style="color:#8b949e; font-size:0.9rem; line-height:1.5;">'
            'Break complex, multi-stage workflows into sequential sub-prompts. '
            'Pass the verified output of Step 1 as context payload into Step 2 to maximize accuracy.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )
    with c_t2:
        st.markdown(
            '<div class="apple-card">'
            '<div class="apple-card-header">🧠 Chain-of-Thought (CoT)</div>'
            '<p style="color:#8b949e; font-size:0.9rem; line-height:1.5;">'
            'Instruct the LLM to <em>"think step-by-step"</em> or output intermediate reasoning inside <code>&lt;thinking&gt;</code> tags. '
            'Drastically improves complex math, logic, and code generation.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )
    with c_t3:
        st.markdown(
            '<div class="apple-card">'
            '<div class="apple-card-header">🚫 Negative Constraints</div>'
            '<p style="color:#8b949e; font-size:0.9rem; line-height:1.5;">'
            'Explicitly state what the model MUST NOT do (e.g., <em>"Do not include conversational preamble"</em> or <em>"Do not fabricate missing facts"</em>).'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )
