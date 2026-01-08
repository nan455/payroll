# ============================================
# FILE 3: database.py (PostgreSQL Version)
# ============================================

import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_config():
    """Get database configuration from environment"""
    # Render provides DATABASE_URL environment variable
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Production (Render)
        return {'database_url': database_url}
    else:
        # Local development (convert to PostgreSQL local)
        return {
            'host': 'localhost',
            'database': 'payroll_system',
            'user': 'postgres',
            'password': 'postgres',
            'port': 5432
        }

def get_db():
    """Create database connection"""
    try:
        config = get_db_config()
        
        if 'database_url' in config:
            # Production - use DATABASE_URL
            conn = psycopg2.connect(config['database_url'])
        else:
            # Development - use individual params
            conn = psycopg2.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                port=config.get('port', 5432)
            )
        
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def dict_cursor(conn):
    """Get dictionary cursor"""
    return conn.cursor(cursor_factory=RealDictCursor)

def test_connection():
    """Test database connection"""
    conn = get_db()
    if conn:
        print("✅ Database connection successful!")
        conn.close()
        return True
    else:
        print("❌ Database connection failed!")
        return False

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                role VARCHAR(100) NOT NULL,
                daily_salary DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status VARCHAR(20) NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
                UNIQUE(employee_id, date)
            )
        ''')
        
        # Create advances table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advances (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER NOT NULL,
                date DATE NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                reason TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_employee ON attendance(employee_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_advances_date ON advances(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_advances_employee ON advances(employee_id)')
        
        conn.commit()
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
