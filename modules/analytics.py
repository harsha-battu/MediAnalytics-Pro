import pandas as pd
import numpy as np

def summarize_visits(df):
    if df.empty:
        return {"total": 0, "daily_average": 0, "monthly_growth": 0.0}
    dates = pd.to_datetime(df["visit_date"])
    total = len(df)
    days = max((dates.max().date() - dates.min().date()).days + 1, 1)
    monthly = dates.dt.to_period("M").value_counts().sort_index()
    growth = 0.0
    if len(monthly) >= 2 and monthly.iloc[-2] != 0:
        growth = (monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2] * 100
    return {"total": total, "daily_average": total / days, "monthly_growth": growth}

def forecast_next_month(df):
    if df.empty:
        return 0
    s = pd.to_datetime(df["visit_date"]).dt.to_period("M").value_counts().sort_index()
    values = s.values.astype(float)
    if len(values) < 2:
        return int(round(values[-1]))
    x = np.arange(len(values))
    slope, intercept = np.polyfit(x, values, 1)
    return max(0, int(round(intercept + slope * len(values))))
