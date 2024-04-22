import os
from app.Managers.ConfigManager import ConfigManager
from app.Managers.LogManager import LogManager
from app.Managers.DbManager import DbManager
from app.Managers.TelegramManager import TelegramManager

DIR = os.path.abspath(os.path.dirname(__file__))

config_manager = ConfigManager(DIR)
log_manager = LogManager(config_manager)
db_manager = DbManager()
telegram_manager = TelegramManager()


# get task list from db
# check time
# if time run task
# get result from task
# send task results






