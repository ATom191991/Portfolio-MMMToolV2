import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "use_sample" not in st.session_state:
    st.session_state.use_sample = True

# Import pages
def show_landing():
    import landing_page

def show_report():
    import report_dashboard

if st.session_state.page == "landing":
    show_landing()
elif st.session_state.page == "report":
    show_report()