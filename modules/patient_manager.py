from database.db_connection import query_df, execute
from modules.data_validation import age_band

def list_patients(search=""):
    return query_df(
        "SELECT patient_id, age, age_band, gender, created_at FROM patients "
        "WHERE CAST(patient_id AS CHAR) LIKE :s ORDER BY patient_id DESC LIMIT 500",
        {"s": f"%{search}%"}
    )

def add_patient(age, gender):
    band = age_band(age)
    return execute("INSERT INTO patients(age, age_band, gender) VALUES(:a,:b,:g)",
                   {"a": int(age), "b": band, "g": gender})

def delete_patient(patient_id):
    execute("DELETE FROM patients WHERE patient_id=:id", {"id": int(patient_id)})
