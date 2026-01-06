from flask import Flask
from database import init_db
from routes import init_routes

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Initialize database
init_db()

# Initialize routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)