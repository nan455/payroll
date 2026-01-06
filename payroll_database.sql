-- ============================================
-- Employee Payroll Management System Database
-- Import this file in phpMyAdmin
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS `payroll_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `payroll_system`;

-- ============================================
-- Table: employees
-- ============================================
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `role` varchar(100) NOT NULL,
  `daily_salary` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample Data for employees
INSERT INTO `employees` (`id`, `name`, `role`, `daily_salary`, `created_at`) VALUES
(1, 'Rajesh Kumar', 'Mason', 800.00, '2024-01-15 10:30:00'),
(2, 'Suresh Patel', 'Carpenter', 900.00, '2024-01-15 10:35:00'),
(3, 'Amit Singh', 'Helper', 500.00, '2024-01-15 10:40:00'),
(4, 'Vijay Sharma', 'Electrician', 1000.00, '2024-01-15 10:45:00'),
(5, 'Ramesh Yadav', 'Plumber', 850.00, '2024-01-15 10:50:00');

-- ============================================
-- Table: attendance
-- ============================================
CREATE TABLE `attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` enum('Present','Absent') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_attendance` (`employee_id`,`date`),
  KEY `employee_id` (`employee_id`),
  KEY `date` (`date`),
  CONSTRAINT `fk_attendance_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample Data for attendance (Last 7 days)
INSERT INTO `attendance` (`employee_id`, `date`, `status`) VALUES
(1, '2025-01-01', 'Present'),
(2, '2025-01-01', 'Present'),
(3, '2025-01-01', 'Present'),
(4, '2025-01-01', 'Absent'),
(5, '2025-01-01', 'Present'),
(1, '2025-01-02', 'Present'),
(2, '2025-01-02', 'Present'),
(3, '2025-01-02', 'Absent'),
(4, '2025-01-02', 'Present'),
(5, '2025-01-02', 'Present'),
(1, '2025-01-03', 'Present'),
(2, '2025-01-03', 'Present'),
(3, '2025-01-03', 'Present'),
(4, '2025-01-03', 'Present'),
(5, '2025-01-03', 'Absent');

-- ============================================
-- Table: advances
-- ============================================
CREATE TABLE `advances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_id` (`employee_id`),
  KEY `date` (`date`),
  CONSTRAINT `fk_advances_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample Data for advances
INSERT INTO `advances` (`employee_id`, `date`, `amount`, `reason`) VALUES
(1, '2025-01-02', 2000.00, 'Medical emergency'),
(2, '2025-01-03', 1500.00, 'Festival advance'),
(3, '2025-01-01', 1000.00, 'Personal loan'),
(5, '2025-01-04', 3000.00, 'House repair');

-- ============================================
-- Useful Views for Quick Reports
-- ============================================

-- View: Current Month Attendance Summary
CREATE OR REPLACE VIEW `current_month_attendance` AS
SELECT 
    e.id,
    e.name,
    e.role,
    e.daily_salary,
    COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_days,
    COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as absent_days,
    (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) as gross_salary
FROM employees e
LEFT JOIN attendance a ON e.id = a.employee_id 
    AND MONTH(a.date) = MONTH(CURRENT_DATE())
    AND YEAR(a.date) = YEAR(CURRENT_DATE())
GROUP BY e.id;

-- View: Current Month Payroll Summary
CREATE OR REPLACE VIEW `current_month_payroll` AS
SELECT 
    e.id,
    e.name,
    e.role,
    COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_days,
    e.daily_salary,
    (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) as gross_salary,
    COALESCE(SUM(adv.amount), 0) as total_advance,
    ((COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) - COALESCE(SUM(adv.amount), 0)) as net_salary
FROM employees e
LEFT JOIN attendance a ON e.id = a.employee_id 
    AND MONTH(a.date) = MONTH(CURRENT_DATE())
    AND YEAR(a.date) = YEAR(CURRENT_DATE())
LEFT JOIN advances adv ON e.id = adv.employee_id 
    AND MONTH(adv.date) = MONTH(CURRENT_DATE())
    AND YEAR(adv.date) = YEAR(CURRENT_DATE())
GROUP BY e.id;

-- ============================================
-- Stored Procedures
-- ============================================

-- Procedure: Get Weekly Payroll
DELIMITER $$
CREATE PROCEDURE `get_weekly_payroll`(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT 
        e.id,
        e.name,
        e.role,
        COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_days,
        e.daily_salary,
        (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) as gross_salary,
        COALESCE(SUM(adv.amount), 0) as total_advance,
        ((COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) - COALESCE(SUM(adv.amount), 0)) as net_salary
    FROM employees e
    LEFT JOIN attendance a ON e.id = a.employee_id 
        AND a.date BETWEEN start_date AND end_date
    LEFT JOIN advances adv ON e.id = adv.employee_id 
        AND adv.date BETWEEN start_date AND end_date
    GROUP BY e.id
    ORDER BY e.id;
END$$
DELIMITER ;

-- Procedure: Get Monthly Report
DELIMITER $$
CREATE PROCEDURE `get_monthly_report`(
    IN report_month INT,
    IN report_year INT
)
BEGIN
    SELECT 
        e.id,
        e.name,
        e.role,
        COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present_days,
        e.daily_salary,
        (COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) as gross_salary,
        COALESCE(SUM(adv.amount), 0) as total_advance,
        ((COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * e.daily_salary) - COALESCE(SUM(adv.amount), 0)) as net_salary
    FROM employees e
    LEFT JOIN attendance a ON e.id = a.employee_id 
        AND MONTH(a.date) = report_month
        AND YEAR(a.date) = report_year
    LEFT JOIN advances adv ON e.id = adv.employee_id 
        AND MONTH(adv.date) = report_month
        AND YEAR(adv.date) = report_year
    GROUP BY e.id
    ORDER BY e.id;
END$$
DELIMITER ;

-- ============================================
-- Indexes for Better Performance
-- ============================================
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_status ON attendance(status);
CREATE INDEX idx_advances_date ON advances(date);
CREATE INDEX idx_employees_role ON employees(role);

-- ============================================
-- Database Successfully Created!
-- You can now manage all data through phpMyAdmin
-- ============================================