import streamlit as st
import pandas as pd
from database.db_connection import query_df
from modules.visit_manager import add_visit
from modules.authentication import require_role
require_role("Admin","Staff")
st.title("Synthetic Data Import")
st.warning("Import only synthetic data. Expected columns: patient_id, department_id, visit_date, visit_type.")
upload=st.file_uploader("Upload CSV or Excel",type=["csv","xlsx"])
if upload:
    try:
        df=pd.read_csv(upload) if upload.name.endswith(".csv") else pd.read_excel(upload)
        st.dataframe(df.head(20),use_container_width=True)
        required={"patient_id","department_id","visit_date","visit_type"}
        if not required.issubset(df.columns): st.error(f"Missing columns: {required-set(df.columns)}")
        elif st.button("Import validated rows"):
            patients=set(query_df("SELECT patient_id FROM patients").patient_id)
            depts=set(query_df("SELECT department_id FROM departments").department_id)
            good=0; errors=[]
            for i,row in df.iterrows():
                try:
                    if int(row.patient_id) not in patients or int(row.department_id) not in depts: raise ValueError("Unknown patient or department")
                    add_visit(row.patient_id,row.department_id,pd.to_datetime(row.visit_date).to_pydatetime(),str(row.visit_type))
                    good+=1
                except Exception as ex: errors.append(f"Row {i+2}: {ex}")
            st.success(f"Imported {good} rows.")
            if errors: st.warning("\n".join(errors[:20]))
    except Exception as e: st.error(f"Could not read file: {e}")
