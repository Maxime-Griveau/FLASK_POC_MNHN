import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')

# Charger le fichier .env
if os.path.exists(dotenv_path):
    dotenv.load_dotenv(dotenv_path)
else:
    print(f"WARNING: .env file not found at {dotenv_path}")

class Config():
    DEBUG = os.environ.get("DEBUG", True)
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
