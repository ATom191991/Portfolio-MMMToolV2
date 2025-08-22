import streamlit as st

def landing_page():
    st.set_page_config(page_title="MMM ROI Dashboard", layout="centered")

    st.markdown(
        """
        <style>
        .main {
            background-color: #F7FAFC;
        }
        .big-title {
            font-size: 2.8em;
            font-weight: bold;
            color: #212A3E;
            text-align: center;
            margin-bottom: 0.1em;
        }
        .subtitle {
            font-size: 1.3em;
            color: #374151;
            text-align: center;
            margin-bottom: 1.5em;
        }
        .info-card {
            background-color: #E6ECF5;
            border-radius: 10px;
            padding: 1.2em;
            margin-bottom: 1em;
            box-shadow: 0 2px 8px #e7eaf0;
        }
        .feature-list {
            color: #334155;
            font-size: 1.1em;
            margin-left: 2em;
        }
        .cta-btn {
            width: 100%;
            height: 3em;
            font-size: 1.15em;
            font-weight: bold;
            border-radius: 8px;
            margin-bottom: 0.8em;
            background-color: #212A3E !important;
            color: #F7FAFC !important;
            border: None;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='big-title'>Marketing Mix Modeling ROI Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Unlock actionable insights from your marketing data.<br>Upload your campaign, analyze your spend, and download a professional report.</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-card'><b>🚀 What can you do with this dashboard?</b>", unsafe_allow_html=True)
    st.markdown(
        """
        <ul class='feature-list'>
            <li>Run instant ROI analysis with sample data or your own Excel/CSV</li>
            <li>Visualize your marketing spend, revenue, and ROI by channel</li>
            <li>Interactively optimize budget allocation</li>
            <li>Forecast revenue based on spend changes</li>
            <li>Download a detailed PDF dashboard for sharing</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='info-card'><b>💡 How it works:</b>", unsafe_allow_html=True)
    st.markdown(
        """
        <ol class='feature-list'>
            <li>Choose "Run Sample Report" to see a demo</li>
            <li>Or "Upload Your Data" to analyze your own campaign</li>
            <li>Explore the interactive dashboard and download your report</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        run_demo = st.button("Run Sample Report", key="sample", help="See a demo with sample data")
    with col2:
        upload_data = st.button("Upload Your Data", key="upload", help="Start with your own Excel/CSV")

    if run_demo:
        st.session_state.page = "report"
        st.session_state.use_sample = True
        st.rerun()
    elif upload_data:
        st.session_state.page = "report"
        st.session_state.use_sample = False
        st.rerun()

    st.markdown(
        """
        <hr>
        <div style='text-align: center; color: #7B8FA1; font-size: 0.98em; margin-top: 2em;'>
            Built by <a href="https://github.com/ATom191991" style="color: #212A3E;">ATom191991</a> | Powered by Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
