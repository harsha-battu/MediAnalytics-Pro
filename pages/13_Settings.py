import streamlit as st
from modules.authentication import require_role
from utils.backup import create_backup
require_role("Admin")
st.title("Settings & Database Backup")
st.info("Backup requires mysqldump installed and available on the server PATH.")
if st.button("Create SQL backup"):
    try:
        path=create_backup("reports/medi_analytics_backup.sql")
        with open(path,"rb") as f:
            st.download_button("Download database backup",f.read(),"medi_analytics_backup.sql","application/sql")
    except Exception as e: st.error(f"Backup failed: {e}")
