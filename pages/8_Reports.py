import streamlit as st
from database.db_connection import query_df
from modules.report_generator import to_excel,to_pdf
from modules.authentication import require_role
require_role("Admin","Staff","Analyst")
st.title("Reports & Downloads")
try:
    report=query_df("""SELECT v.visit_id,v.patient_id,d.department_name,v.visit_date,v.visit_type,v.status
                      FROM visits v JOIN departments d ON d.department_id=v.department_id
                      ORDER BY v.visit_date DESC""")
    st.dataframe(report,use_container_width=True,hide_index=True)
    st.download_button("Download CSV",report.to_csv(index=False).encode("utf-8"),"hospital_visits.csv","text/csv")
    st.download_button("Download Excel",to_excel(report),"hospital_visits.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("Download PDF",to_pdf(report),"hospital_visits.pdf","application/pdf")
except Exception as e: st.error(f"Report error: {e}")
