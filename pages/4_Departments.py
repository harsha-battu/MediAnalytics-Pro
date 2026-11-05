import streamlit as st
from database.db_connection import query_df, execute
from modules.authentication import require_role
require_role("Admin","Staff","Analyst")
st.title("Department Management")
try:
    if st.session_state.user["role"] == "Admin":
        with st.form("dept"):
            name = st.text_input("Department name")
            desc = st.text_input("Description")
            if st.form_submit_button("Add department") and name.strip():
                execute("INSERT INTO departments(department_name,description) VALUES(:n,:d)", {"n":name.strip(),"d":desc})
                st.success("Department added."); st.rerun()
    df = query_df("""SELECT d.department_id,d.department_name,d.description,COUNT(v.visit_id) visit_count
                      FROM departments d LEFT JOIN visits v ON v.department_id=d.department_id
                      GROUP BY d.department_id,d.department_name,d.description
                      ORDER BY visit_count DESC""")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty: st.bar_chart(df.set_index("department_name")["visit_count"])
except Exception as e: st.error(f"Database error: {e}")
