from database.db_connection import query_df, execute

def list_visits(start=None, end=None, department_id=None):
    sql = """SELECT v.visit_id, v.patient_id, d.department_name, v.visit_date,
                     v.visit_type, v.status
              FROM visits v JOIN departments d ON d.department_id=v.department_id
              WHERE (:start IS NULL OR v.visit_date >= :start)
                AND (:end IS NULL OR v.visit_date < :end)
                AND (:dept IS NULL OR v.department_id=:dept)
              ORDER BY v.visit_date DESC LIMIT 5000"""
    return query_df(sql, {"start": start, "end": end, "dept": department_id})

def add_visit(patient_id, department_id, visit_date, visit_type):
    return execute("""INSERT INTO visits(patient_id,department_id,visit_date,visit_type)
                      VALUES(:p,:d,:dt,:t)""",
                   {"p": int(patient_id), "d": int(department_id), "dt": visit_date, "t": visit_type})
