__import__('pysqlite3') 
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
import traceback

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Load .env file at the very top of the script
load_dotenv()

# --- 1. Initialize Session State ---
if 'email_content' not in st.session_state:
    st.session_state.email_content = ""

# --- 2. Cached Functions to Load Heavy Objects ---
@st.cache_resource
def get_chain():
    return Chain()

# --- 3. Main App UI ---
st.set_page_config(layout="wide", page_title="Cold Job Email Generator", page_icon="📧")
st.title("📧 Cold Job Email Generator")

# --- NEW: Sidebar to collect personal job applicant information ---
st.sidebar.header("👤 Your Information")
your_name = st.sidebar.text_input("Your Name", "Suvadip Khanra")
your_status = st.sidebar.text_input("Your Background/Status", "a final-year B.Tech (CSE) student")
your_passion = st.sidebar.text_input("Your Passion/Specialty", "full-stack development")
your_projects = st.sidebar.text_area("Key Projects & Achievements", "Built an AI-powered mock interview platform (React, Firebase) and a responsive restaurant website. Participated in the Smart India Hackathon.")
your_skills = st.sidebar.text_input("Relevant Skills", "React, Node.js, and databases")
your_phone = st.sidebar.text_input("Your Phone Number")
your_links = st.sidebar.text_input("Portfolio/GitHub/LinkedIn URL")
# -----------------------------------------------------------------

# Load the singleton chain object from cache
chain = get_chain()

job_description_text = st.text_area("Paste the Full Job Description Here", height=250, placeholder="Paste the job description you are applying for...")

# --- 4. Button Logic to Run the Process ---
if st.button("Generate Email"):
    if not job_description_text:
        st.error("Please paste a job description.")
    else:
        with st.spinner("Crafting your personalized email..."):
            try:
                # Store the result in session state
                st.session_state.email_content = chain.write_application_mail(
                    job_description=clean_text(job_description_text),
                    your_name=your_name,
                    your_status=your_status,
                    your_passion=your_passion,
                    your_projects=your_projects,
                    your_skills=your_skills,
                    your_phone=your_phone,
                    your_links=your_links
                )
            
            except Exception as e:
                st.error("An error occurred while processing.")
                st.exception(e)

# --- 5. Display Results ---
if st.session_state.email_content:
    st.markdown("---")
    st.subheader("Generated Application Email")
    st.code(st.session_state.email_content, language='markdown')