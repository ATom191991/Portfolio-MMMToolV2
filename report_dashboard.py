import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from backend.mmm import run_mmm_and_calculate_roi

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

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
kpi_col1.metric("Total Spend", f"${total_spend:,.0f}")
kpi_col2.metric("Revenue Attributed", f"${revenue_attributed:,.0f}")
kpi_col3.metric("ROI (Avg)", f"{roi_mean:.2f}")
kpi_col4.metric("Incremental Sales", f"${incremental_sales:,.0f}")
kpi_col5.metric("MER", f"{mer:.2f}")

st.markdown("---")

chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    st.subheader("ROI by Channel (Bar Chart)")
    fig, ax = plt.subplots(figsize=(4, 3))
    roi_df["ROI"].plot(kind="bar", color="dodgerblue", ax=ax)
    ax.set_ylabel("ROI")
    st.pyplot(fig)

with chart_col2:
    st.subheader("Channel Contribution (Pie Chart)")
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    roi_df["Total Spend"].plot(kind="pie", autopct="%.1f%%", startangle=90, ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

with chart_col3:
    st.subheader("ROI Trend Over Time")
    if "Date" in df.columns:
        trend_df = df.groupby("Date")["Sales"].sum()
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        trend_df.plot(ax=ax3, marker="o")
        ax3.set_ylabel("Sales")
        ax3.set_xlabel("Date")
        st.pyplot(fig3)
    else:
        st.info("Date column not available for time trend.")

st.markdown("---")

analytics_col1, analytics_col2, analytics_col3 = st.columns(3)

with analytics_col1:
    st.subheader("Spend vs Revenue Curve")
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    ax4.scatter(df["Spend"], df["Sales"], color="mediumseagreen")
    ax4.set_xlabel("Spend")
    ax4.set_ylabel("Sales")
    st.pyplot(fig4)

with analytics_col2:
    st.subheader("Marginal ROI (Bar Chart)")
    fig5, ax5 = plt.subplots(figsize=(4, 3))
    roi_df["ROI"].plot(kind="bar", color="orange", ax=ax5)
    ax5.set_ylabel("Marginal ROI")
    st.pyplot(fig5)

with analytics_col3:
    st.subheader("Budget Mix: Current vs Optimized")
    optimized_spend = roi_df["Total Spend"].copy()
    best_channel = roi_df["ROI"].idxmax()
    optimized_spend[best_channel] *= 1.1
    fig6, ax6 = plt.subplots(figsize=(4, 3))
    ax6.bar(roi_df.index, roi_df["Total Spend"], label="Current", alpha=0.6)
    ax6.bar(roi_df.index, optimized_spend, label="Optimized", alpha=0.6)
    ax6.set_ylabel("Spend")
    ax6.legend()
    st.pyplot(fig6)

st.markdown("---")

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

    fig7, ax7 = plt.subplots(figsize=(6, 3))
    ax7.bar(new_spend.keys(), new_spend.values(), color="slateblue")
    ax7.set_ylabel("Adjusted Spend")
    st.pyplot(fig7)

st.markdown("---")

bottom_col1, bottom_col2, bottom_col3 = st.columns(3)

with bottom_col1:
    st.subheader("Short-term vs Long-term ROI (Heatmap)")
    if "Date" in df.columns:
        pivot = df.pivot_table(index="Date", columns="Channel", values="Sales", aggfunc="sum").fillna(0)
        fig8, ax8 = plt.subplots(figsize=(4, 3))
        sns.heatmap(pivot, annot=True, cmap="coolwarm", ax=ax8)
        st.pyplot(fig8)
    else:
        st.info("Date column not available for heatmap.")

with bottom_col2:
    st.subheader("CAC by Channel")
    cac = roi_df["Total Spend"] / roi_df["Incremental Revenue"].replace(0, np.nan)
    st.dataframe(pd.DataFrame({"CAC": cac}).style.format({"CAC": "{:.2f}"}))

with bottom_col3:
    st.subheader("LTV/CAC + Retention Impact")
    retention_rate = 0.75
    ltv = roi_df["Incremental Revenue"] * retention_rate
    ltv_cac = ltv / cac.replace(0, np.nan)
    st.dataframe(pd.DataFrame({"LTV/CAC": ltv_cac}).style.format({"LTV/CAC": "{:.2f}"}))

st.markdown("---")

st.subheader("Full ROI Table")
st.dataframe(roi_df.style.format({"ROI": "{:.2f}", "Total Spend": "{:,.0f}", "Incremental Revenue": "{:,.0f}"}))