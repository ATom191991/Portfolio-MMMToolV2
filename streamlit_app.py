import streamlit as st
import pandas as pd
from backend.mmm import run_mmm_and_calculate_roi
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os

SAMPLE_PATH = "data/sample_marketing_data.csv"

st.set_page_config(page_title="MMM ROI Calculator", layout="wide")

st.title("Market Mix Modelling (MMM) ROI Dashboard")

# --- Sidebar options ---
st.sidebar.header("Options")
option = st.sidebar.radio("Choose an option:", ["Run Sample Data", "Upload Excel"])

# --- File load section ---
if option == "Run Sample Data":
    st.success("Using built-in sample data.")
    df = pd.read_csv(SAMPLE_PATH)
    show_input = True
elif option == "Upload Excel":
    st.subheader("Expected Format")
    sample_df = pd.read_csv(SAMPLE_PATH)
    st.dataframe(sample_df.head())
    uploaded_file = st.file_uploader("Upload your marketing data (.xlsx or .csv)", type=["xlsx", "csv"])
    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        show_input = True
    else:
        df = None
        show_input = False
else:
    df = None
    show_input = False

if show_input and df is not None:
    st.subheader("Your Data")
    st.dataframe(df.head())

    # --- MMM calculation ---
    try:
        roi_df, model = run_mmm_and_calculate_roi(df)
    except Exception as e:
        st.error(f"Error in MMM calculation: {e}")
        st.stop()

    st.subheader("ROI by Channel")
    st.dataframe(roi_df.style.format({"ROI": "{:.2f}", "Total Spend": "{:,.0f}", "Incremental Revenue": "{:,.0f}"}))

    # --- Advanced Insights ---
    st.subheader("Insights")
    best_channel = roi_df["ROI"].idxmax()
    best_value = roi_df.loc[best_channel, "ROI"]
    worst_channel = roi_df["ROI"].idxmin()
    worst_value = roi_df.loc[worst_channel, "ROI"]
    avg_roi = roi_df["ROI"].mean()

    st.markdown(f"""
    - <span style='color:green'><b>Best ROI:</b> {best_channel} ({best_value:.2f})</span>
    - <span style='color:red'><b>Worst ROI:</b> {worst_channel} ({worst_value:.2f})</span>
    - <b>Average ROI across channels:</b> {avg_roi:.2f}
    """, unsafe_allow_html=True)

    if best_value > 1:
        st.success(f"Great! The {best_channel} channel is generating more incremental revenue than spend (ROI > 1). Consider increasing its budget.")
    if worst_value < 0:
        st.warning(f"Warning: The {worst_channel} channel has negative ROI. Consider reviewing or reducing spend on this channel.")

    # --- Visualizations ---
    st.subheader("Visualizations")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**ROI by Channel (Bar Chart)**")
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        roi_df["ROI"].plot(kind="bar", ax=ax1, color="dodgerblue")
        ax1.axhline(0, color='grey', linestyle='--')
        ax1.set_ylabel("ROI")
        ax1.set_xlabel("Channel")
        st.pyplot(fig1)

    with col2:
        st.markdown("**Spend by Channel (Pie Chart)**")
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        roi_df["Total Spend"].plot(kind="pie", autopct="%.1f%%", startangle=90, ax=ax2)
        ax2.set_ylabel("")
        st.pyplot(fig2)

    st.markdown("**Correlation Heatmap**")
    try:
        wide = df.pivot_table(index="Date", columns="Channel", values="Spend", aggfunc="sum").fillna(0)
        corr = wide.corr()
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
        st.pyplot(fig3)
    except Exception:
        st.info("Correlation heatmap not available for this data.")

    # --- PDF Dashboard Download ---
    st.markdown("---")
    st.header("Download Your PDF Dashboard")

    def create_pdf_dashboard(roi_df, best_channel, best_value, worst_channel, worst_value, avg_roi, fig1, fig2, fig3):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover page
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(0, 15, "MMM ROI Dashboard", ln=1, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "Automated Marketing Mix Modeling Report", ln=1, align='C')
        pdf.ln(10)

        # Insights
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Insights", ln=1)
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 8, f"Best ROI: {best_channel} ({best_value:.2f})", ln=1)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 8, f"Worst ROI: {worst_channel} ({worst_value:.2f})", ln=1)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"Average ROI: {avg_roi:.2f}", ln=1)
        pdf.ln(4)
        if best_value > 1:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 8, f"The {best_channel} channel is generating more incremental revenue than spend (ROI > 1).", ln=1)
        if worst_value < 0:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 8, f"The {worst_channel} channel has negative ROI. Consider reviewing its budget.", ln=1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

        # ROI Table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "ROI Table", ln=1)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(50, 8, "Channel", border=1)
        pdf.cell(40, 8, "Total Spend", border=1)
        pdf.cell(60, 8, "Incremental Revenue", border=1)
        pdf.cell(30, 8, "ROI", border=1, ln=1)
        pdf.set_font("Arial", '', 12)
        for idx, row in roi_df.iterrows():
            pdf.cell(50, 8, str(idx), border=1)
            pdf.cell(40, 8, f"{row['Total Spend']:,.0f}", border=1)
            pdf.cell(60, 8, f"{row['Incremental Revenue']:,.0f}", border=1)
            pdf.cell(30, 8, f"{row['ROI']:.2f}", border=1, ln=1)
        pdf.ln(5)

        # Charts: Save plots to images and insert
        def fig_to_img(fig):
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            return buf

        # Bar chart
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "ROI by Channel (Bar Chart)", ln=1)
        img1 = fig_to_img(fig1)
        pdf.image(img1, w=170)
        pdf.ln(5)

        # Pie chart
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Spend by Channel (Pie Chart)", ln=1)
        img2 = fig_to_img(fig2)
        pdf.image(img2, w=120)
        pdf.ln(5)

        # Correlation heatmap
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Correlation Heatmap", ln=1)
        img3 = fig_to_img(fig3)
        pdf.image(img3, w=120)
        pdf.ln(5)

        # Return as bytes
        pdf_bytes = pdf.output(dest="S").encode("latin1")
        return pdf_bytes

    if st.button("Generate PDF Dashboard"):
        # Re-create charts for PDF (to avoid Streamlit/Matplotlib issues)
        # Bar chart
        fig1_pdf, ax1_pdf = plt.subplots(figsize=(5, 3))
        roi_df["ROI"].plot(kind="bar", ax=ax1_pdf, color="dodgerblue")
        ax1_pdf.axhline(0, color='grey', linestyle='--')
        ax1_pdf.set_ylabel("ROI")
        ax1_pdf.set_xlabel("Channel")
        plt.tight_layout()

        # Pie chart
        fig2_pdf, ax2_pdf = plt.subplots(figsize=(5, 3))
        roi_df["Total Spend"].plot(kind="pie", autopct="%.1f%%", startangle=90, ax=ax2_pdf)
        ax2_pdf.set_ylabel("")
        plt.tight_layout()

        # Correlation heatmap
        fig3_pdf, ax3_pdf = plt.subplots(figsize=(6, 4))
        sns.heatmap(wide.corr(), annot=True, cmap="coolwarm", ax=ax3_pdf)
        plt.tight_layout()

        pdf_bytes = create_pdf_dashboard(
            roi_df, best_channel, best_value, worst_channel, worst_value, avg_roi,
            fig1_pdf, fig2_pdf, fig3_pdf
        )
        st.download_button(
            label="Download PDF Dashboard",
            data=pdf_bytes,
            file_name="mmm_dashboard.pdf",
            mime="application/pdf"
        )

else:
    st.info("Please select 'Run Sample Data' or upload your Excel/CSV file to begin.")