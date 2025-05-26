
import streamlit as st
import openai
from datetime import date
import os

# Set your OpenAI API key (securely via env var or secrets)
openai.api_key = os.getenv("OPENAI_API_KEY") or "your_openai_api_key"

st.set_page_config(page_title="SOW Generator", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("SOWGen")
    st.radio("Navigate", ["Dashboard", "New SOW", "Saved SOWs", "Templates", "Reports", "Settings"])

# Page Title
st.title("📄 New Statement of Work (SOW)")

# Layout Split
col1, col2 = st.columns([2, 1])

# ======================
# 🔧 Main SOW Input Form
# ======================
with col1:
    st.header("🛠️ Project Information")
    sow_type = st.selectbox("SOW Template Type", [
        "Digital Transformation",
        "Core Banking Modernization",
        "Cloud Migration",
        "Custom SOW"
    ])
    client_name = st.text_input("Client Name")
    project_name = st.text_input("Project Name")
    scope = st.text_area("Project Scope Summary", height=120)
    deliverables = st.text_area("Deliverables", height=100)
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date")
    milestones = st.text_area("Milestones", height=80)
    commercials = st.text_area("Commercials / Fees", height=60)
    payment_schedule = st.text_area("Payment Schedule", height=60)
    dependencies = st.text_area("Dependencies", height=60)
    assumptions = st.text_area("Assumptions", height=60)
    approval_contact = st.text_input("Approval Contact Name/Title")

    if st.button("Generate SOW"):
        sow_text = f"""
        ## Statement of Work (SOW)
        
        **Client:** {client_name}  
        **Project Name:** {project_name}  
        **Template Type:** {sow_type}  
        **Start Date:** {start_date}  
        **End Date:** {end_date}  

        ### Scope  
        {scope}

        ### Deliverables  
        {deliverables}

        ### Milestones  
        {milestones}

        ### Commercials  
        {commercials}

        ### Payment Schedule  
        {payment_schedule}

        ### Dependencies  
        {dependencies}

        ### Assumptions  
        {assumptions}

        ### Approval Contact  
        {approval_contact}
        """
        st.success("✅ SOW generated successfully!")
        st.markdown("### 📄 Preview")
        st.code(sow_text, language="markdown")
        st.download_button("📥 Download SOW", sow_text, file_name="sow_document.txt")

# ========================
# 🤖 GenAI Assistance Tool
# ========================
with col2:
    st.header("🤖 AI Assistance")
    assist_mode = st.selectbox("Select Help Mode", ["Suggest a clause", "Rewrite section", "Explain section"])
    user_input = st.text_area("Describe your request or paste content", height=200)

    if st.button("Ask AI"):
        if not user_input.strip():
            st.warning("Please enter some content or a question.")
        else:
            prompt_templates = {
                "Suggest a clause": f"Write a professional clause for a Statement of Work based on:\n{user_input}",
                "Rewrite section": f"Rewrite this SOW section more clearly and formally:\n{user_input}",
                "Explain section": f"Explain this SOW section in business-friendly language:\n{user_input}",
            }
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_templates[assist_mode]}],
                    temperature=0.4
                )
                ai_reply = response.choices[0].message.content
                st.success("AI Response")
                st.write(ai_reply)
            except Exception as e:
                st.error(f"Error from OpenAI: {e}")
