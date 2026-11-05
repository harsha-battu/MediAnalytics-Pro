import streamlit as st
from modules.authentication import require_role
from modules.patient_manager import list_patients, add_patient, delete_patient
require_role("Admin","Staff")
st.title("Patient Records")
st.caption("Use synthetic/demo data only.")
with st.form("add_patient"):
    age = st.number_input("Age", 0, 120, 25)
    gender = st.selectbox("Gender", ["Not specified","Female","Male","Other"])
    submitted = st.form_submit_button("Add patient")
    if submitted:
        try:
            pid = add_patient(age, gender)
            st.success(f"Patient created: P-{pid}")
            st.rerun()
        except Exception as e: st.error(str(e))
search = st.text_input("Search by patient ID")
try:
    df = list_patients(search)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty:
        pid = st.number_input("Patient ID to delete", min_value=1, step=1)
        if st.button("Delete patient"):
            try: delete_patient(pid); st.success("Deleted."); st.rerun()
            except Exception as e: st.error(f"Delete failed: {e}. Existing visits/appointments may reference this patient.")
except Exception as e: st.error(f"Database error: {e}")
