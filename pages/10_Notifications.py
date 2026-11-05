import streamlit as st
from modules.notification_manager import notifications,add_notification
from modules.authentication import require_role
require_role("Admin","Staff","Analyst")
st.title("Notification Center")
if st.session_state.user["role"]=="Admin":
    msg=st.text_input("New operational notification")
    if st.button("Publish") and msg.strip():
        add_notification(msg.strip()); st.success("Notification published."); st.rerun()
try: st.dataframe(notifications(),use_container_width=True,hide_index=True)
except Exception as e: st.error(f"Notification error: {e}")
