import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    def __init__(self, DIR):
        self.app_path = DIR

        self.debug = bool(int(os.getenv("DEBUG", False)))

        self.db_host = str(os.getenv("DB_HOST"))
        self.db_port = str(os.getenv("DB_PORT"))
        self.db_name = str(os.getenv("DB_NAME"))
        self.db_user = str(os.getenv("DB_USER"))
        self.db_pass = str(os.getenv("DB_PASS"))

        self.log_level = str(os.getenv("LOG_LEVEL", "INFO")) if not self.debug else "DEBUG"
        self.log_dir = f"{self.app_path}/logs"
        self.log_file = f"{self.app_path}/logs/{str(os.getenv('LOG_FILE', 'app.log'))}"

        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
        if not os.path.isfile(self.log_file):
            open(self.log_file, "w").close()


