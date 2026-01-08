"""
Configuration file for different environments
Supports: Local Development, PythonAnywhere, Railway, Render
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    # PythonAnywhere format: username$database_name
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'payroll_system')
    
    @staticmethod
    def get_db_config():
        """Returns database configuration dictionary"""
        return {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME
        }

class DevelopmentConfig(Config):
    """Local development configuration - XAMPP"""
    DEBUG = True
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''  # XAMPP default has no password
    DB_NAME = 'payroll_system'
    
    @staticmethod
    def get_db_config():
        """Returns database configuration for XAMPP"""
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Change if you set a password in XAMPP
            'database': 'payroll_system'
        }

class PythonAnywhereConfig(Config):
    """PythonAnywhere hosting configuration"""
    DEBUG = False
    # Example: yourusername.mysql.pythonanywhere-services.com
    DB_HOST = os.environ.get('DB_HOST', 'Nandacumaar.mysql.pythonanywhere-services.com')
    DB_USER = os.environ.get('DB_USER', 'Nandacumaar')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Selvamviji6@')
    DB_NAME = os.environ.get('DB_NAME', 'Nandacumaar$payroll_system')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Choose configuration based on environment
config = {
    'development': DevelopmentConfig,
    'pythonanywhere': PythonAnywhereConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment variable"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])