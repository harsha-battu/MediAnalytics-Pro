from database.db_connection import query_df, execute

def notifications():
    return query_df("SELECT * FROM notifications ORDER BY created_at DESC LIMIT 200")

def add_notification(message):
    execute("INSERT INTO notifications(message) VALUES(:m)", {"m": message})
