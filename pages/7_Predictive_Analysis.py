import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import query_df
from modules.analytics import forecast_next_month
from modules.authentication import require_role
require_role("Admin","Analyst")
st.title("Predictive Analysis")
st.caption("Forecasts are estimates for educational operational planning, not guaranteed values.")
try:
    df=query_df("SELECT visit_date FROM visits ORDER BY visit_date")
    if df.empty: st.info("Add historical visits to generate a forecast.")
    else:
        prediction=forecast_next_month(df)
        st.metric("Estimated visits next month",f"{prediction:,}")
        monthly=pd.to_datetime(df.visit_date).dt.to_period("M").value_counts().sort_index()
        hist=monthly.rename_axis("month").reset_index(name="actual_visits")
        hist["month"]=hist.month.astype(str)
        st.plotly_chart(px.bar(hist,x="month",y="actual_visits",title="Historical monthly visits"),use_container_width=True)
        st.caption("Method: linear trend fitted to monthly visit counts. More historical data improves stability.")
except Exception as e: st.error(f"Forecast error: {e}")
