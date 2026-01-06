# ============================================
# MYSQL VERSION - Updated Python Files
# ============================================

# ============================================
# FILE: database.py (MySQL Version)
# ============================================

import mysql.connector
from mysql.connector import Error

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Change to your MySQL username
    'password': '',           # Change to your MySQL password
    'database': 'payroll_system'
}

def get_db():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database - Not needed as we import SQL file in phpMyAdmin"""
    pass

