 #============================================
# FILE 4: models.py (PostgreSQL Version)
# ============================================

from database import get_db, dict_cursor
from database import get_db
from datetime import datetime
from psycopg2.extras import RealDictCursor

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
        cursor = dict_cursor(conn)
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
        cursor = dict_cursor(conn)
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
            cursor.execute('SELECT COUNT(*) FROM employees')
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
                   ON CONFLICT (employee_id, date) 
                   DO UPDATE SET status = EXCLUDED.status''',
                (employee_id, date, status)
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
        cursor = dict_cursor(conn)
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
                SELECT COUNT(*) 
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
                SELECT COUNT(*) 
                FROM attendance
                WHERE employee_id = %s 
                AND EXTRACT(MONTH FROM date) = %s 
                AND EXTRACT(YEAR FROM date) = %s
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
        cursor = dict_cursor(conn)
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
                SELECT COALESCE(SUM(amount), 0)
                FROM advances
                WHERE employee_id = %s AND date BETWEEN %s AND %s
            ''', (employee_id, start_date, end_date))
            result = cursor.fetchone()
            return float(result[0]) if result else 0
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
                SELECT COALESCE(SUM(amount), 0)
                FROM advances
                WHERE employee_id = %s 
                AND EXTRACT(MONTH FROM date) = %s 
                AND EXTRACT(YEAR FROM date) = %s
            ''', (employee_id, month, year))
            result = cursor.fetchone()
            return float(result[0]) if result else 0
        finally:
            cursor.close()
            conn.close()

class Site:
    @staticmethod
    def create(site_name, location, client_name, start_date, end_date, total_budget, notes):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO sites (site_name, location, client_name, start_date, 
                   end_date, total_budget, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (site_name, location, client_name, start_date, end_date, total_budget, notes)
            )
            conn.commit()
            return cursor.lastrowid
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
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('SELECT * FROM sites ORDER BY created_at DESC')
            sites = cursor.fetchall()
            return sites
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_id(site_id):
        conn = get_db()
        if not conn:
            return None
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('SELECT * FROM sites WHERE id = %s', (site_id,))
            site = cursor.fetchone()
            return site
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_active_sites():
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM sites WHERE status = 'Active' ORDER BY site_name")
            sites = cursor.fetchall()
            return sites
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(site_id, site_name, location, client_name, start_date, end_date, status, total_budget, notes):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''UPDATE sites SET site_name = %s, location = %s, client_name = %s,
                   start_date = %s, end_date = %s, status = %s, total_budget = %s, notes = %s
                   WHERE id = %s''',
                (site_name, location, client_name, start_date, end_date, status, total_budget, notes, site_id)
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
    def delete(site_id):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM sites WHERE id = %s', (site_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_summary(site_id):
        conn = get_db()
        if not conn:
            return None
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT 
                    s.*,
                    COUNT(DISTINCT sw.employee_id) as total_workers,
                    COALESCE(SUM(sm.total_cost), 0) as total_material_cost,
                    COALESCE(SUM(sm.amount_paid), 0) as total_paid,
                    COALESCE(SUM(sm.amount_balance), 0) as total_balance
                FROM sites s
                LEFT JOIN site_workers sw ON s.id = sw.site_id AND sw.is_active = TRUE
                LEFT JOIN site_materials sm ON s.id = sm.site_id
                WHERE s.id = %s
                GROUP BY s.id
            ''', (site_id,))
            summary = cursor.fetchone()
            return summary
        finally:
            cursor.close()
            conn.close()

class SiteWorker:
    @staticmethod
    def assign_worker(site_id, employee_id, assigned_date, role_at_site):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO site_workers (site_id, employee_id, assigned_date, role_at_site)
                   VALUES (%s, %s, %s, %s)''',
                (site_id, employee_id, assigned_date, role_at_site)
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
    def remove_worker(site_worker_id, removed_date):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''UPDATE site_workers SET is_active = FALSE, removed_date = %s
                   WHERE id = %s''',
                (removed_date, site_worker_id)
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
    def get_site_workers(site_id):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT sw.*, e.name, e.role as employee_role, e.daily_salary
                FROM site_workers sw
                JOIN employees e ON sw.employee_id = e.id
                WHERE sw.site_id = %s AND sw.is_active = TRUE
                ORDER BY sw.assigned_date DESC
            ''', (site_id,))
            workers = cursor.fetchall()
            return workers
        finally:
            cursor.close()
            conn.close()

class MaterialCategory:
    @staticmethod
    def get_all():
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('SELECT * FROM material_categories ORDER BY category_name')
            categories = cursor.fetchall()
            return categories
        finally:
            cursor.close()
            conn.close()

class SiteMaterial:
    @staticmethod
    def create(site_id, material_category_id, material_name, quantity, unit, rate_per_unit, 
               supplier_name, sent_date, bill_number, notes):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            total_cost = float(quantity) * float(rate_per_unit)
            cursor.execute(
                '''INSERT INTO site_materials 
                   (site_id, material_category_id, material_name, quantity, unit, 
                    rate_per_unit, total_cost, supplier_name, sent_date, bill_number, 
                    amount_balance, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (site_id, material_category_id, material_name, quantity, unit, 
                 rate_per_unit, total_cost, supplier_name, sent_date, bill_number, 
                 total_cost, notes)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_site_materials(site_id):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT sm.*, mc.category_name
                FROM site_materials sm
                JOIN material_categories mc ON sm.material_category_id = mc.id
                WHERE sm.site_id = %s
                ORDER BY sm.sent_date DESC
            ''', (site_id,))
            materials = cursor.fetchall()
            return materials
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_id(material_id):
        conn = get_db()
        if not conn:
            return None
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT sm.*, mc.category_name, s.site_name
                FROM site_materials sm
                JOIN material_categories mc ON sm.material_category_id = mc.id
                JOIN sites s ON sm.site_id = s.id
                WHERE sm.id = %s
            ''', (material_id,))
            material = cursor.fetchone()
            return material
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_pending_payments(site_id=None):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if site_id:
                cursor.execute('''
                    SELECT sm.*, mc.category_name, s.site_name
                    FROM site_materials sm
                    JOIN material_categories mc ON sm.material_category_id = mc.id
                    JOIN sites s ON sm.site_id = s.id
                    WHERE sm.site_id = %s AND sm.payment_status != 'Paid'
                    ORDER BY sm.sent_date DESC
                ''', (site_id,))
            else:
                cursor.execute('''
                    SELECT sm.*, mc.category_name, s.site_name
                    FROM site_materials sm
                    JOIN material_categories mc ON sm.material_category_id = mc.id
                    JOIN sites s ON sm.site_id = s.id
                    WHERE sm.payment_status != 'Paid'
                    ORDER BY sm.sent_date DESC
                ''')
            materials = cursor.fetchall()
            return materials
        finally:
            cursor.close()
            conn.close()

class MaterialPayment:
    @staticmethod
    def create(site_material_id, payment_date, amount, payment_mode, reference_number, notes):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            # Insert payment
            cursor.execute(
                '''INSERT INTO material_payments 
                   (site_material_id, payment_date, amount, payment_mode, reference_number, notes)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (site_material_id, payment_date, amount, payment_mode, reference_number, notes)
            )
            
            # Update material payment status
            cursor.execute('''
                UPDATE site_materials sm
                SET 
                    amount_paid = COALESCE((
                        SELECT SUM(amount) 
                        FROM material_payments 
                        WHERE site_material_id = sm.id
                    ), 0),
                    amount_balance = sm.total_cost - COALESCE((
                        SELECT SUM(amount) 
                        FROM material_payments 
                        WHERE site_material_id = sm.id
                    ), 0),
                    payment_status = CASE
                        WHEN COALESCE((
                            SELECT SUM(amount) 
                            FROM material_payments 
                            WHERE site_material_id = sm.id
                        ), 0) = 0 THEN 'Pending'
                        WHEN COALESCE((
                            SELECT SUM(amount) 
                            FROM material_payments 
                            WHERE site_material_id = sm.id
                        ), 0) < sm.total_cost THEN 'Partial'
                        ELSE 'Paid'
                    END
                WHERE sm.id = %s
            ''', (site_material_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_material_payments(material_id):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT * FROM material_payments
                WHERE site_material_id = %s
                ORDER BY payment_date DESC
            ''', (material_id,))
            payments = cursor.fetchall()
            return payments
        finally:
            cursor.close()
            conn.close()

class SiteExpense:
    @staticmethod
    def create(site_id, expense_date, expense_type, description, amount, paid_to, payment_mode):
        conn = get_db()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO site_expenses 
                   (site_id, expense_date, expense_type, description, amount, paid_to, payment_mode)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (site_id, expense_date, expense_type, description, amount, paid_to, payment_mode)
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
    def get_site_expenses(site_id, start_date=None, end_date=None):
        conn = get_db()
        if not conn:
            return []
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            if start_date and end_date:
                cursor.execute('''
                    SELECT * FROM site_expenses
                    WHERE site_id = %s AND expense_date BETWEEN %s AND %s
                    ORDER BY expense_date DESC
                ''', (site_id, start_date, end_date))
            else:
                cursor.execute('''
                    SELECT * FROM site_expenses
                    WHERE site_id = %s
                    ORDER BY expense_date DESC
                    LIMIT 50
                ''', (site_id,))
            expenses = cursor.fetchall()
            return expenses
        finally:
            cursor.close()
            conn.close()