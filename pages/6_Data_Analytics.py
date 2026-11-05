import streamlit as st
import plotly.express as px
from database.db_connection import query_df
from modules.authentication import require_role
require_role("Admin","Staff","Analyst")
st.title("Advanced Data Analytics")
try:
    df = query_df("""SELECT v.visit_date,v.visit_type,d.department_name,p.age_band
                    FROM visits v JOIN departments d ON d.department_id=v.department_id
                    JOIN patients p ON p.patient_id=v.patient_id""")
    if df.empty: st.info("No data available yet.")
    else:
        start,end = st.date_input("Date range", value=(df.visit_date.min().date(),df.visit_date.max().date()))
        f = df[(df.visit_date.dt.date>=start)&(df.visit_date.dt.date<=end)]
        c1,c2 = st.columns(2)
        c1.plotly_chart(px.histogram(f,x="department_name",title="Department workload"),use_container_width=True)
        c2.plotly_chart(px.pie(f,names="age_band",title="Age-band distribution"),use_container_width=True)
        st.plotly_chart(px.histogram(f,x="visit_type",color="visit_type",title="Visit type analysis"),use_container_width=True)
        daily=f.assign(day=f.visit_date.dt.date).groupby("day").size().reset_index(name="visits")
        st.plotly_chart(px.line(daily,x="day",y="visits",markers=True,title="Daily visit trend"),use_container_width=True)
except Exception as e: st.error(f"Analytics error: {e}")
