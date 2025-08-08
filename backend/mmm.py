import pandas as pd
import statsmodels.api as sm

def run_mmm_and_calculate_roi(df):
    # Data validation
    required_cols = {"Date", "Channel", "Spend", "Sales"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Data must contain columns: {required_cols}")

    wide = df.pivot_table(index="Date", columns="Channel", values="Spend", aggfunc="sum").fillna(0)
    wide["Sales"] = df.groupby("Date")["Sales"].sum()
    X = wide.drop("Sales", axis=1)
    y = wide["Sales"]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    coefs = model.params.drop("const")
    total_spend = wide.drop("Sales", axis=1).sum()
    incremental_rev = coefs * total_spend
    roi = (incremental_rev - total_spend) / total_spend
    roi_df = pd.DataFrame({
        "Total Spend": total_spend,
        "Incremental Revenue": incremental_rev,
        "ROI": roi
    })
    return roi_df, model