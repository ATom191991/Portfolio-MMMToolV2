import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from backend.mmm import run_mmm_and_calculate_roi

# --- Custom CSS for theme ---
st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #F2F2F2 !important;
        color: #111 !important;
    }
    .block-container {
        background-color: #E6F0FF !important;
        border-radius: 12px;
        box-shadow: 0 2px 8px #cfd8dc;
        padding: 1.5em 1em 1.5em 1em;
        margin-bottom: 1.5em;
    }
    .kpi-block {
        background-color: #E6F0FF !important;
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 0.5em;
        box-shadow: 0 1px 4px #cfd8dc;
        text-align: center;
    }
    .small-font {
        font-size: 0.9em;
        color: #666;
        margin-top: 1em;
    }
    .stMetric {
        color: #111 !important;
    }
    .roi-table-block {
        background-color: #E6F0FF !important;
        border-radius: 12px;
        box-shadow: 0 2px 8px #cfd8dc;
        padding: 2em 1em 2em 1em;
        margin-bottom: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

def report_dashboard():
    SAMPLE_PATH = "data/sample_marketing_data.csv"

    if st.session_state.get("use_sample", True):
        df = pd.read_csv(SAMPLE_PATH)
        data_source = "Sample Data"
    else:
        uploaded_file = st.file_uploader("Upload your marketing data (.xlsx or .csv)", type=["xlsx", "csv"])
        if uploaded_file:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            data_source = uploaded_file.name
        else:
            st.info("Please upload your marketing data to proceed.")
            st.stop()

    roi_df, model = run_mmm_and_calculate_roi(df)
    total_spend = roi_df["Total Spend"].sum()
    revenue_attributed = roi_df["Incremental Revenue"].sum()
    roi_mean = roi_df["ROI"].mean()
    incremental_sales = roi_df["Incremental Revenue"].sum()
    mer = revenue_attributed / total_spend if total_spend else 0

    st.title("Marketing Mix Modeling Dashboard")
    st.markdown(f"**Data Source:** {data_source}")

    # --- First Row: KPIs in blocks ---
    st.markdown("<div class='block-container'>", unsafe_allow_html=True)
    kpi_cols = st.columns(5)
    kpi_labels = ["Total Spend", "Revenue Attributed", "ROI (Avg)", "Incremental Sales", "MER"]
    kpi_values = [
        f"${total_spend:,.0f}",
        f"${revenue_attributed:,.0f}",
        f"{roi_mean:.2f}",
        f"${incremental_sales:,.0f}",
        f"{mer:.2f}"
    ]
    for idx in range(5):
        with kpi_cols[idx]:
            st.markdown(f"<div class='kpi-block'><span style='font-size:1em;font-weight:600'>{kpi_labels[idx]}</span><br><span style='font-size:1.5em;font-weight:bold'>{kpi_values[idx]}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Second Row: Full ROI Table only ---
    st.markdown("<div class='roi-table-block'>", unsafe_allow_html=True)
    st.subheader("Full ROI Table")
    st.dataframe(roi_df.style.format({"ROI": "{:.2f}", "Total Spend": "{:,.0f}", "Incremental Revenue": "{:,.0f}"}))
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Third Row: Channel Contribution Pie & Spend vs Revenue Bar ---
    third_row = st.columns(2)
    # Pie Chart block
    with third_row[0]:
        st.markdown("<div class='block-container'>", unsafe_allow_html=True)
        st.subheader("Channel Contribution (Pie Chart)")
        fig, ax = plt.subplots(figsize=(4, 3))
        roi_df["Total Spend"].plot(kind="pie", autopct="%.1f%%", startangle=90, ax=ax, colors=sns.color_palette("pastel"))
        ax.set_ylabel("")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    # Spend vs Revenue Bar block
    with third_row[1]:
        st.markdown("<div class='block-container'>", unsafe_allow_html=True)
        st.subheader("Spend vs Revenue (Bar Chart)")
        # Group spend and sales by channel
        grouped = df.groupby("Channel")[["Spend", "Sales"]].sum()
        fig2, ax2 = plt.subplots(figsize=(4,3))
        colors = sns.color_palette("husl", grouped.shape[0])
        ax2.bar(grouped.index, grouped["Spend"], label="Spend", color=colors, alpha=0.7)
        ax2.bar(grouped.index, grouped["Sales"], label="Revenue", color=colors, alpha=0.4, bottom=grouped["Spend"])
        ax2.set_ylabel("Amount ($)")
        ax2.legend()
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Fourth Row: Forecast Section (unchanged), with assumption note ---
    st.markdown("<div class='block-container'>", unsafe_allow_html=True)
    controls_col1, controls_col2 = st.columns([1, 2])
    with controls_col1:
        st.subheader("Adjust Spend")
        new_spend = {}
        for channel in roi_df.index:
            val = st.slider(f"{channel} Spend", int(roi_df.loc[channel, "Total Spend"]*0.5), int(roi_df.loc[channel, "Total Spend"]*1.5), int(roi_df.loc[channel, "Total Spend"]))
            new_spend[channel] = val
    with controls_col2:
        st.subheader("Forecasted Revenue & ROI")
        forecasted_rev = sum(new_spend[ch] * roi_df.loc[ch, "ROI"] for ch in roi_df.index)
        st.metric("Forecasted Revenue", f"${forecasted_rev:,.0f}")
        st.metric("Forecasted ROI", f"{forecasted_rev / sum(new_spend.values()):.2f}" if sum(new_spend.values()) else "N/A")
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        colors = sns.color_palette("husl", len(new_spend))
        ax3.bar(new_spend.keys(), new_spend.values(), color=colors)
        ax3.set_ylabel("Adjusted Spend")
        st.pyplot(fig3)
    st.markdown(
        "<div class='small-font'>Assumption: ROI is assumed to remain constant with changes in spend. Real-world effects like diminishing returns or saturation are not accounted for in this simple model.</div>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Removed fifth and sixth rows as per instruction ---