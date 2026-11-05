from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import streamlit as st
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

@st.cache_resource
def get_engine():
    url = URL.create(
        "mysql+pymysql", username=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        query={"charset": "utf8mb4"}
    )
    return create_engine(url, pool_pre_ping=True, pool_recycle=3600)

def query_df(sql, params=None):
    with get_engine().connect() as conn:
        return __import__("pandas").read_sql(text(sql), conn, params=params or {})

def execute(sql, params=None):
    with get_engine().begin() as conn:
        result = conn.execute(text(sql), params or {})
        return result.lastrowid
