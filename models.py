from database import get_db

class Employee:
    @staticmethod
    def create(name, role, daily_salary):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO employees (name, role, daily_salary) VALUES (%s, %s, %s)',
                (name, role, daily_salary)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_all():
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM employees ORDER BY id DESC')
            employees = cursor.fetchall()
            return employees
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_id(emp_id):
        conn = get_db()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM employees WHERE id = %s', (emp_id,))
            employee = cursor.fetchone()
            return employee
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(emp_id, name, role, daily_salary):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE employees SET name = %s, role = %s, daily_salary = %s WHERE id = %s',
                (name, role, daily_salary, emp_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(emp_id):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM employees WHERE id = %s', (emp_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def count():
        conn = get_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as count FROM employees')
            count = cursor.fetchone()[0]
            return count
        finally:
            cursor.close()
            conn.close()

class Attendance:
    @staticmethod
    def mark(employee_id, date, status):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO attendance (employee_id, date, status) 
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE status = %s''',
                (employee_id, date, status, status)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_date(date):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT a.*, e.name, e.role 
                FROM attendance a
                JOIN employees e ON a.employee_id = e.id
                WHERE a.date = %s
            ''', (date,))
            attendance = cursor.fetchall()
            return attendance
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_week_attendance(employee_id, start_date, end_date):
        conn = get_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) as present_days
                FROM attendance
                WHERE employee_id = %s AND date BETWEEN %s AND %s AND status = 'Present'
            ''', (employee_id, start_date, end_date))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_month_attendance(employee_id, month, year):
        conn = get_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) as present_days
                FROM attendance
                WHERE employee_id = %s 
                AND MONTH(date) = %s 
                AND YEAR(date) = %s
                AND status = 'Present'
            ''', (employee_id, month, year))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()

class Advance:
    @staticmethod
    def create(employee_id, date, amount, reason):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO advances (employee_id, date, amount, reason) VALUES (%s, %s, %s, %s)',
                (employee_id, date, amount, reason)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_all():
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT a.*, e.name 
                FROM advances a
                JOIN employees e ON a.employee_id = e.id
                ORDER BY a.date DESC
            ''')
            advances = cursor.fetchall()
            return advances
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_week_advance(employee_id, start_date, end_date):
        conn = get_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) as total_advance
                FROM advances
                WHERE employee_id = %s AND date BETWEEN %s AND %s
            ''', (employee_id, start_date, end_date))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_month_advance(employee_id, month, year):
        conn = get_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) as total_advance
                FROM advances
                WHERE employee_id = %s 
                AND MONTH(date) = %s 
                AND YEAR(date) = %s
            ''', (employee_id, month, year))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()
