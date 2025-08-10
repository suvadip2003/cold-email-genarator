# --- FIX for sqlite3 version on Streamlit Cloud ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ----------------------------------------------------

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
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- 2. Cached Functions to Load Heavy Objects ---
@st.cache_resource
def get_chain():
    print("--- Initializing Chain (should run only once) ---")
    return Chain()

@st.cache_resource
def get_portfolio():
    print("--- Initializing Portfolio (should run only once) ---")
    p = Portfolio()
    p.load_portfolio()
    return p

# --- 3. Main App UI ---
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
st.title("📧 Cold Mail Generator")

# --- NEW: Create a sidebar to collect user information ---
st.sidebar.header("👤 Your Information")
user_name = st.sidebar.text_input("Your Name", "Mohan")
user_role = st.sidebar.text_input("Your Role", "Business Development Executive")
user_company = st.sidebar.text_input("Your Company", "AtliQ")
company_description = st.sidebar.text_area(
    "Your Company Description",
    "AtliQ is an AI & Software Consulting company dedicated to facilitating the seamless integration of business processes through automated tools."
)
# ---------------------------------------------------------

# Load the singleton objects from cache
chain = get_chain()
portfolio = get_portfolio()

url_input = st.text_input(
    "Enter a Job Posting URL:", 
    value="https://careers.nike.com/director-software-engineering-data-analytics-and-intelligence-itc/job/R-66928"
)

# --- 4. Button Logic to Run the Process ---
if st.button("Generate Email"):
    if not url_input:
        st.error("Please enter a URL.")
    else:
        with st.spinner("Analyzing job posting and generating emails..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                st.session_state.jobs = chain.extract_jobs(data)
            
            except Exception as e:
                st.error("An error occurred while processing.")
                st.exception(e)

# --- 5. Display Results ---
if st.session_state.jobs:
    st.markdown("---")
    for job in st.session_state.jobs:
        skills = job.get('skills', [])
        links = portfolio.query_links(skills)
        
        # --- NEW: Pass user info from the sidebar to the email generation function ---
        email = chain.write_mail(
            job=job, 
            links=links,
            user_name=user_name,
            user_role=user_role,
            user_company=user_company,
            company_description=company_description
        )
        
        st.subheader(f"Generated Email for: {job.get('role', 'N/A')}")
        st.code(email, language='markdown')
        st.markdown("---")