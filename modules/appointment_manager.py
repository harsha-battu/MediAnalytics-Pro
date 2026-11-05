from database.db_connection import query_df, execute

def get_appointments():
    return query_df("""SELECT a.appointment_id,a.patient_id,d.department_name,
        a.appointment_date,a.status,a.notes FROM appointments a
        JOIN departments d ON d.department_id=a.department_id
        ORDER BY a.appointment_date DESC LIMIT 1000""")

def create_appointment(patient_id, department_id, appointment_date, notes=""):
    return execute("""INSERT INTO appointments(patient_id,department_id,appointment_date,notes)
        VALUES(:p,:d,:dt,:n)""", {"p":int(patient_id),"d":int(department_id),"dt":appointment_date,"n":notes})

def update_status(appointment_id, status):
    execute("UPDATE appointments SET status=:s WHERE appointment_id=:id",
            {"s":status,"id":int(appointment_id)})
