def eda_agent(df):
    numeric_df = df.select_dtypes(include="number")

    unstacked = numeric_df.corr().unstack()

    seen = set()
    deduped = {}
    for (a, b), v in unstacked.items():
        if a == b:
            continue
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        deduped[(a, b)] = v

    top = sorted(deduped.items(), key=lambda x: abs(x[1]), reverse=True)[:5]

    corr_clean = {
        f"{k[0]} vs {k[1]}": round(v, 3)
        for k, v in top
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

