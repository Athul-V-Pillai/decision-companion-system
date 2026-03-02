"""
Configuration module for Decision Companion System
"""

import os

# Flask Configuration
DEBUG = os.environ.get('FLASK_DEBUG', True)
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Server Configuration
HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
PORT = int(os.environ.get('FLASK_PORT', 5000))

# CORS Configuration (if needed for cross-origin requests)
CORS_ENABLED = os.environ.get('CORS_ENABLED', False)

# Logging Configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
