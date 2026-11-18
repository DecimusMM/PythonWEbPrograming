import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "dev-secret-key"
DEBUG = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload size
PRODUCTS_DB_PATH = os.path.join(BASE_DIR, "data", "products.json")
CONTACTS_LOG_PATH = os.path.join(BASE_DIR, "logs", "contacts.log")
