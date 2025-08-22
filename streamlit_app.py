import streamlit as st
from landing_page import landing_page
from report_dashboard import report_dashboard

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "use_sample" not in st.session_state:
    st.session_state.use_sample = True

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "report":
    report_dashboard()