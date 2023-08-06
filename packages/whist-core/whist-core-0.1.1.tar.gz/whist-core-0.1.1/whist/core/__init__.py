"""
Retrieves envs for the whist core module.
"""
import os

ALGORITHM = os.getenv('ALGORITHM', 'HS256')
SECRET_KEY = os.getenv('SECRET_KEY', 'geheim')
