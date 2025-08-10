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
# This prevents the "KeyError" by ensuring the keys always exist.
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

# --- 2. Cached Functions to Load Heavy Objects ---
# This uses caching to load the Chain and Portfolio objects only ONCE.
# It makes the app fast and avoids re-initializing on every click.
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

# Load the singleton objects from cache
chain = get_chain()
portfolio = get_portfolio()

url_input = st.text_input(
    "Enter a Job Posting URL:", 
    value="https://careers.nike.com/director-software-engineering-data-analytics-and-intelligence-itc/job/R-66928"
)

# --- 4. Button Logic to Run the Process ---
# This section's only job is to run the logic and store the result in session_state.
if st.button("Generate Email"):
    if not url_input:
        st.error("Please enter a URL.")
    else:
        with st.spinner("Analyzing job posting and generating emails..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                # Store the extracted jobs in session state
                st.session_state.jobs = chain.extract_jobs(data)
            
            except Exception as e:
                st.error("An error occurred while processing.")
                st.exception(e)

# --- 5. Display Results ---
# This section's only job is to display any results that are stored in session_state.
# This decouples the logic from the display.
if st.session_state.jobs:
    st.markdown("---")
    for job in st.session_state.jobs:
        skills = job.get('skills', [])
        links = portfolio.query_links(skills)
        email = chain.write_mail(job, links)
        
        st.subheader(f"Generated Email for: {job.get('role', 'N/A')}")
        st.code(email, language='markdown')
        st.markdown("---")