"""
Database Migration Script for Site Management Module
Run this locally or on Render to create site management tables
"""

import os
import psycopg2
from psycopg2 import sql

# Get database URL from environment or prompt
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found!")
    print("Please enter your Render DATABASE_URL:")
    DATABASE_URL = input("DATABASE_URL: ").strip()

if not DATABASE_URL:
    print("❌ No DATABASE_URL provided. Exiting.")
    exit(1)

print(f"🔗 Using database: {DATABASE_URL[:30]}...")  # Show first 30 chars only

def migrate_database():
    """Create all site management tables"""
    
    conn = None
    cursor = None
    
    print("🔄 Connecting to database...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        print("🔄 Creating tables...")
        
        # Table 1: Sites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sites (
                id SERIAL PRIMARY KEY,
                site_name VARCHAR(200) NOT NULL,
                location VARCHAR(255) NOT NULL,
                client_name VARCHAR(150),
                start_date DATE,
                end_date DATE,
                status VARCHAR(50) DEFAULT 'Active',
                total_budget DECIMAL(15,2),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'sites' created")
        
        # Table 2: Site Workers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_workers (
                id SERIAL PRIMARY KEY,
                site_id INTEGER NOT NULL,
                employee_id INTEGER NOT NULL,
                assigned_date DATE NOT NULL,
                removed_date DATE,
                role_at_site VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        """)
        print("✅ Table 'site_workers' created")
        
        # Table 3: Material Categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS material_categories (
                id SERIAL PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT
            )
        """)
        print("✅ Table 'material_categories' created")
        
        # Insert categories
        categories = [
            ('Cement', 'Cement and binding materials'),
            ('Steel', 'Steel rods, bars, and materials'),
            ('Sand', 'River sand, M-sand'),
            ('Bricks', 'Red bricks, concrete blocks'),
            ('Aggregate', 'Stone chips, gravel'),
            ('Paint', 'Interior and exterior paints'),
            ('Plumbing', 'Pipes, fittings, sanitary'),
            ('Electrical', 'Wires, switches, fittings'),
            ('Wood', 'Timber, plywood, doors'),
            ('Hardware', 'Nails, screws, tools'),
            ('Other', 'Miscellaneous materials')
        ]
        
        for cat_name, cat_desc in categories:
            cursor.execute("""
                INSERT INTO material_categories (category_name, description)
                VALUES (%s, %s)
                ON CONFLICT (category_name) DO NOTHING
            """, (cat_name, cat_desc))
        print("✅ Material categories inserted")
        
        # Table 4: Site Materials
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_materials (
                id SERIAL PRIMARY KEY,
                site_id INTEGER NOT NULL,
                material_category_id INTEGER NOT NULL,
                material_name VARCHAR(200) NOT NULL,
                quantity DECIMAL(10,2) NOT NULL,
                unit VARCHAR(50) NOT NULL,
                rate_per_unit DECIMAL(10,2) NOT NULL,
                total_cost DECIMAL(15,2) NOT NULL,
                supplier_name VARCHAR(150),
                sent_date DATE NOT NULL,
                bill_number VARCHAR(100),
                amount_paid DECIMAL(15,2) DEFAULT 0,
                amount_balance DECIMAL(15,2),
                payment_status VARCHAR(50) DEFAULT 'Pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
                FOREIGN KEY (material_category_id) REFERENCES material_categories(id)
            )
        """)
        print("✅ Table 'site_materials' created")
        
        # Table 5: Material Payments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS material_payments (
                id SERIAL PRIMARY KEY,
                site_material_id INTEGER NOT NULL,
                payment_date DATE NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                payment_mode VARCHAR(50),
                reference_number VARCHAR(100),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (site_material_id) REFERENCES site_materials(id) ON DELETE CASCADE
            )
        """)
        print("✅ Table 'material_payments' created")
        
        # Table 6: Site Expenses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_expenses (
                id SERIAL PRIMARY KEY,
                site_id INTEGER NOT NULL,
                expense_date DATE NOT NULL,
                expense_type VARCHAR(100) NOT NULL,
                description TEXT,
                amount DECIMAL(10,2) NOT NULL,
                paid_to VARCHAR(150),
                payment_mode VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE
            )
        """)
        print("✅ Table 'site_expenses' created")
        
        # Create Indexes
        print("🔄 Creating indexes...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_site_workers_site ON site_workers(site_id)",
            "CREATE INDEX IF NOT EXISTS idx_site_workers_employee ON site_workers(employee_id)",
            "CREATE INDEX IF NOT EXISTS idx_site_materials_site ON site_materials(site_id)",
            "CREATE INDEX IF NOT EXISTS idx_site_materials_date ON site_materials(sent_date)",
            "CREATE INDEX IF NOT EXISTS idx_site_materials_status ON site_materials(payment_status)",
            "CREATE INDEX IF NOT EXISTS idx_material_payments_material ON material_payments(site_material_id)",
            "CREATE INDEX IF NOT EXISTS idx_site_expenses_site ON site_expenses(site_id)",
            "CREATE INDEX IF NOT EXISTS idx_site_expenses_date ON site_expenses(expense_date)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        print("✅ All indexes created")
        
        # Commit changes
        conn.commit()
        
        print("\n🎉 SUCCESS! All tables created successfully!")
        print("\n📊 Tables created:")
        print("  1. sites")
        print("  2. site_workers")
        print("  3. material_categories (with 11 categories)")
        print("  4. site_materials")
        print("  5. material_payments")
        print("  6. site_expenses")
        print("\n✅ Database is ready for site management!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check DATABASE_URL is correct")
        print("2. Make sure 'employees' table exists first")
        print("3. Check database connection is working")
        if conn:
            conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    print("=" * 50)
    print("🏗️  SITE MANAGEMENT DATABASE MIGRATION")
    print("=" * 50)
    print()
    
    migrate_database()
    
    print("\n" + "=" * 50)
    print("Migration completed!")
    print("=" * 50)