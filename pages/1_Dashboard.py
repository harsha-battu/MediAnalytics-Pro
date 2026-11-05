import streamlit as st
import plotly.express as px
from database.db_connection import query_df
from modules.analytics import summarize_visits
from modules.authentication import require_role

require_role("Admin","Staff","Analyst")
st.title("Executive Dashboard")
st.caption("HOSPITAL OPERATIONAL OVERVIEW · SYNTHETIC DEMO DATA")
try:
    visits = query_df("""SELECT visit_id, visit_date, visit_type, department_id
                         FROM visits ORDER BY visit_date""")
    departments = query_df("SELECT department_id, department_name FROM departments")
    appts = query_df("SELECT status FROM appointments")
    summary = summarize_visits(visits)
    today = __import__("datetime").date.today()
    today_count = (visits.visit_date.dt.date == today).sum() if not visits.empty else 0
    a,b,c,d = st.columns(4)
    a.metric("Total patient visits", f"{summary['total']:,}")
    b.metric("Today's visits", f"{today_count:,}")
    c.metric("Active departments", len(departments))
    d.metric("Average daily visits", f"{summary['daily_average']:.1f}")
    e,f = st.columns(2)
    e.metric("Monthly visit growth", f"{summary['monthly_growth']:.1f}%")
    completed = (appts.status == "Completed").mean()*100 if not appts.empty else 0
    f.metric("Appointment completion", f"{completed:.1f}%")
    if not visits.empty:
        visits["month"] = visits.visit_date.dt.to_period("M").astype(str)
        monthly = visits.groupby("month").size().reset_index(name="visits")
        st.plotly_chart(px.line(monthly, x="month", y="visits", markers=True,
            title="Monthly visit trends", template="plotly_white"), use_container_width=True)
        workload = visits.merge(departments, on="department_id").groupby("department_name").size().reset_index(name="visits")
        st.plotly_chart(px.bar(workload, x="department_name", y="visits",
            title="Department workload", template="plotly_white"), use_container_width=True)
    else:
        st.info("No visits yet. Add synthetic records from Visit Management or import sample data.")
except Exception as exc:
    st.error(f"Could not load dashboard: {exc}")
