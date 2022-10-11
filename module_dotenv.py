import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

secret_key = os.getenv("SECRET_KEY")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

''' команды для запуска
makemigrations
migrate auth
migrate
'''