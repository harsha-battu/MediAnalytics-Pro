"""Database backup helper. Requires mysqldump installed and available on PATH."""
import subprocess
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def create_backup(path):
    cmd = ["mysqldump", "-h", DB_HOST, "-P", str(DB_PORT), "-u", DB_USER,
           f"-p{DB_PASSWORD}", DB_NAME]
    with open(path, "wb") as output:
        subprocess.run(cmd, stdout=output, check=True)
    return path
