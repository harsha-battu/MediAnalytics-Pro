CREATE DATABASE IF NOT EXISTS medi_analytics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE medi_analytics;

CREATE TABLE IF NOT EXISTS departments (
  department_id INT AUTO_INCREMENT PRIMARY KEY,
  department_name VARCHAR(100) NOT NULL UNIQUE,
  description VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patients (
  patient_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  age INT NOT NULL,
  age_band VARCHAR(20) NOT NULL,
  gender VARCHAR(30) DEFAULT 'Not specified',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (age BETWEEN 0 AND 120)
);

CREATE TABLE IF NOT EXISTS visits (
  visit_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  patient_id BIGINT NOT NULL,
  department_id INT NOT NULL,
  visit_date DATETIME NOT NULL,
  visit_type VARCHAR(40) NOT NULL,
  status VARCHAR(30) DEFAULT 'Completed',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id),
  INDEX idx_visit_date (visit_date),
  INDEX idx_visit_department (department_id)
);

CREATE TABLE IF NOT EXISTS appointments (
  appointment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  patient_id BIGINT NOT NULL,
  department_id INT NOT NULL,
  appointment_date DATETIME NOT NULL,
  status VARCHAR(30) DEFAULT 'Scheduled',
  notes VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id),
  INDEX idx_appointment_date (appointment_date)
);

CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('Admin','Staff','Analyst') NOT NULL DEFAULT 'Staff',
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
  notification_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  message VARCHAR(500) NOT NULL,
  status VARCHAR(30) DEFAULT 'Unread',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
  log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NULL,
  action VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);
