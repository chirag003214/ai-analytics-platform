def eda_agent(df):
    numeric_df = df.select_dtypes(include="number")

    corr = (
        numeric_df.corr()
        .unstack()
        .sort_values(ascending=False)
        .drop_duplicates()
        .head(5)
    )

    corr_clean = {
        f"{k[0]} vs {k[1]}": round(v, 3)
        for k, v in corr.items()
        if k[0] != k[1]
    }

    return {
        "shape": df.shape,
        "missing_pct": df.isnull().mean().round(3).to_dict(),
        "numeric_summary": (
            numeric_df.describe()
            .loc[["mean", "std", "min", "max"]]
            .round(3)
            .to_dict()
        ),
        "top_correlations": corr_clean
    }

