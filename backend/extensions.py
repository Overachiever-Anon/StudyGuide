"""
Declares the extensions used in the application. 

This file defines the extension instances that are used across the application.
These instances are initialized in the application factory to avoid circular imports
and issues with the application context.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create extension instances
db = SQLAlchemy()
bcrypt = Bcrypt()

