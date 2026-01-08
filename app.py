# ============================================
# FILE 5: app.py (Simplified for Render)
# ============================================

from flask import Flask
from database import init_db, test_connection
from routes import init_routes
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database tables
print("Initializing database...")
init_db()

# Test connection
print("Testing database connection...")
test_connection()

# Initialize routes
init_routes(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)