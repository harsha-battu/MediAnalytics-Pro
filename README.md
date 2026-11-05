# MediAnalytics Pro
**Hospital Patient Data Analysis & Operational Intelligence System**  
Intermediate-level B.Tech AIML project built with Python, Streamlit, MySQL, Pandas, NumPy and Plotly.

> Educational project only. Use synthetic data exclusively. This is an operational analytics demo, not a clinical decision-support system.

## Features
- Executive dashboard with visit KPIs and interactive Plotly charts
- Patient records (create, search, list, delete)
- Appointment booking and status tracking
- Department workload management
- Visit capture and visit analytics
- Linear-trend next-month visit estimate
- CSV, Excel and PDF reports
- Synthetic CSV/Excel import
- Admin, Staff and Analyst roles with bcrypt password hashes
- Audit log, notification center and SQL backup helper
- MySQL schema with keys and indexes

## 1. Requirements
- Python 3.10+
- MySQL Server 8+
- `mysqldump` for database backup
- Windows, macOS or Linux

## 2. Install and configure
```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then set your MySQL host, port, database, username and password. Do not commit `.env`.

Create the database and tables:
```bash
mysql -u root -p < database/create_tables.sql
```

## 3. Create the first administrator
Generate a bcrypt hash:
```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'ChangeThisPassword!', bcrypt.gensalt()).decode())"
```
Copy the printed hash and run this SQL in MySQL (replace the hash):
```sql
USE medi_analytics;
INSERT INTO users(username,password_hash,role)
VALUES ('admin', '$2b$12$PASTE_GENERATED_HASH_HERE', 'Admin');

INSERT INTO departments(department_name,description) VALUES
('General Medicine','General outpatient services'),
('Cardiology','Heart and circulatory services'),
('Orthopedics','Bone and joint services'),
('Neurology','Nervous system services'),
('Dental','Dental outpatient services');
```
Choose a strong unique password. The placeholder hash is not a working credential.

## 4. Run
From the project root:
```bash
streamlit run app.py
```
Streamlit opens the local website in your browser. Use the administrator account created above.

## 5. Suggested demo workflow
1. Log in as Admin.
2. Create departments if you have not already.
3. Add several synthetic patients in Patient Records.
4. Record visits and book appointments.
5. Explore Dashboard, Analytics and Predictive Analysis.
6. Download CSV, Excel and PDF reports.
7. Create a Staff or Analyst account in User Management and demonstrate role restrictions.

## CSV import format
The import module expects these columns:
`patient_id, department_id, visit_date, visit_type`

Patient and department IDs must already exist. Example date: `2026-11-04 10:30:00`.

## Security and privacy notes
- Never enter real patient names, phone numbers, addresses, diagnoses or medical records.
- Keep `.env` private and rotate credentials.
- Use HTTPS, least-privilege database accounts and regular encrypted backups for any deployment.
- Role checks are implemented in each page; database permissions and deployment hardening are still required for production.
- This is a student demonstration application, not certified hospital software.

## Project structure
```text
MediAnalytics_Pro/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── database/
│   ├── db_connection.py
│   └── create_tables.sql
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Patient_Records.py
│   ├── 3_Appointments.py
│   ├── 4_Departments.py
│   ├── 5_Visit_Management.py
│   ├── 6_Data_Analytics.py
│   ├── 7_Predictive_Analysis.py
│   ├── 8_Reports.py
│   ├── 9_Data_Import.py
│   ├── 10_Notifications.py
│   ├── 11_User_Management.py
│   ├── 12_Audit_Logs.py
│   └── 13_Settings.py
├── modules/
└── utils/
```

## Troubleshooting
- **Can't connect:** confirm MySQL is running and `.env` credentials/database are correct.
- **Access denied:** check the MySQL user has privileges on `medi_analytics`.
- **Unknown database:** run `database/create_tables.sql`.
- **No dashboard data:** create synthetic patients and visits first.
- **PDF export issue:** reinstall `reportlab`; Excel export uses `openpyxl`.
