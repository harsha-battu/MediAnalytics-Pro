import streamlit as st
from datetime import datetime, date, time
from database.db_connection import query_df
from modules.appointment_manager import get_appointments, create_appointment, update_status
from modules.authentication import require_role
require_role("Admin","Staff")
st.title("Appointment Management")
try:
    patients = query_df("SELECT patient_id FROM patients ORDER BY patient_id DESC LIMIT 1000")
    depts = query_df("SELECT department_id, department_name FROM departments ORDER BY department_name")
    if patients.empty or depts.empty: st.info("Create patients and departments before booking.")
    else:
        with st.form("book"):
            p = st.selectbox("Patient ID", patients.patient_id.tolist())
            dmap = dict(zip(depts.department_name, depts.department_id))
            dn = st.selectbox("Department", list(dmap))
            dt = st.date_input("Appointment date", date.today())
            tm = st.time_input("Appointment time", time(9,0))
            notes = st.text_input("Notes (non-clinical)")
            if st.form_submit_button("Book appointment"):
                create_appointment(p, dmap[dn], datetime.combine(dt,tm), notes)
                st.success("Appointment booked."); st.rerun()
    df = get_appointments()
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty:
        aid = st.selectbox("Appointment ID", df.appointment_id.tolist())
        status = st.selectbox("Update status", ["Scheduled","Completed","Cancelled","Rescheduled","No-show"])
        if st.button("Save status"):
            update_status(aid,status); st.success("Status updated."); st.rerun()
except Exception as e: st.error(f"Database error: {e}")
