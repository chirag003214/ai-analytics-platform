import pandas as pd

def kpi_agent(df, date_col, value_col):
    if not isinstance(value_col, str):
        raise TypeError("value_col must be a column name (string)")
    if value_col not in df.columns or date_col not in df.columns:
        raise KeyError("Invalid column selection")

    series = df[value_col]

    series = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip()
    )

    series = pd.to_numeric(series, errors="coerce")

    kpi = pd.DataFrame({
        date_col: df[date_col],
        value_col: series
    }).sort_values(by=date_col)

    kpi["growth"] = series.pct_change().round(3)

    return kpi


