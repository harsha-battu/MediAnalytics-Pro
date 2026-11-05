import streamlit as st
from database.db_connection import query_df
from modules.authentication import require_role
require_role("Admin")
st.title("Audit Logs")
try:
    st.dataframe(query_df("""SELECT l.log_id,u.username,l.action,l.created_at
                            FROM audit_logs l LEFT JOIN users u ON u.user_id=l.user_id
                            ORDER BY l.created_at DESC LIMIT 1000"""),use_container_width=True,hide_index=True)
except Exception as e: st.error(f"Audit log error: {e}")
