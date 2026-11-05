from datetime import datetime

def age_band(age):
    if not 0 <= int(age) <= 120:
        raise ValueError("Age must be between 0 and 120.")
    age = int(age)
    if age <= 12: return "0-12"
    if age <= 19: return "13-19"
    if age <= 35: return "20-35"
    if age <= 59: return "36-59"
    return "60+"

def validate_visit_date(value):
    if isinstance(value, str):
        datetime.fromisoformat(value)
    return value
