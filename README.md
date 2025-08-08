# Market Mix Modelling (MMM) ROI Calculator

This repository provides a simple, extensible web application for Market Mix Modelling (MMM) analysis. The app enables users to upload marketing data (CSV or Excel), perform MMM using regression, and view the Return on Investment (ROI) for each marketing activity/channel. The MVP is built with Python and Streamlit for quick, interactive analysis.

---

## Features

- **Upload marketing data** in CSV or Excel format
- **Form-based UI** for campaign information and data upload
- **Runs Market Mix Modelling** (MMM) using linear regression
- **Calculates ROI** per marketing channel
- **Displays results** in an interactive table
- **Sample data** provided for easy testing
- **Advanced insights** and visualizations (bar, pie, heatmap)
- **Downloadable, well-formatted PDF dashboard**

---

## File Structure

```
.
├── streamlit_app.py             # Main Streamlit app
├── backend/
│   └── mmm.py                   # MMM and ROI calculation logic
├── data/
│   └── sample_marketing_data.csv  # Sample data
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ATom191991/MarketMixModelPF.git
cd MarketMixModelPF
```

### 2. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

- The app will open at [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. Select "Run Sample Data" or upload your marketing data file (`.csv` or `.xlsx`). See the sample data in `/data/sample_marketing_data.csv` for the expected format:

    | Date       | Channel | Spend | Sales  |
    |------------|---------|-------|--------|
    | 2024-01-01 | TV      | 2000  | 12000  |
    | 2024-01-01 | Social  | 1000  | 8000   |
    | 2024-01-01 | Search  | 1500  | 9500   |
    | ...        | ...     | ...   | ...    |

2. Submit to see ROI by channel, advanced insights, and visualizations.
3. Download a well-formatted PDF dashboard of your results.

---

## Deploying Online

You can deploy this app for free using [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/), connect your repo, and deploy.
3. Share your live app’s URL!

---

## Dependencies

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- pandas
- statsmodels
- openpyxl
- fpdf
- matplotlib
- seaborn

All dependencies are listed in `requirements.txt`.

---

## Customization

- You can extend the MMM logic in `backend/mmm.py`
- Add more visualizations or download options in `streamlit_app.py`
- Integrate with databases or authentication as needed

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions, open an issue or contact [ATom191991](https://github.com/ATom191991).