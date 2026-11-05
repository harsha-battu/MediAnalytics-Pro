import streamlit as st
from datetime import datetime, date, time
from database.db_connection import query_df
from modules.visit_manager import list_visits, add_visit
from modules.authentication import require_role
require_role("Admin","Staff")
st.title("Visit Management")
try:
    patients = query_df("SELECT patient_id FROM patients ORDER BY patient_id DESC LIMIT 1000")
    depts = query_df("SELECT department_id,department_name FROM departments ORDER BY department_name")
    if not patients.empty and not depts.empty:
        with st.form("visit"):
            p = st.selectbox("Patient ID", patients.patient_id.tolist())
            mapping = dict(zip(depts.department_name,depts.department_id))
            dname = st.selectbox("Department",list(mapping))
            vd = st.date_input("Visit date",date.today())
            vt = st.time_input("Visit time",time(10,0))
            typ = st.selectbox("Visit type",["OPD","Emergency","Follow-up","Inpatient"])
            if st.form_submit_button("Record visit"):
                add_visit(p,mapping[dname],datetime.combine(vd,vt),typ)
                st.success("Visit recorded."); st.rerun()
    else: st.info("Add at least one patient and one department first.")
    st.dataframe(list_visits(),use_container_width=True,hide_index=True)
except Exception as e: st.error(f"Database error: {e}")
