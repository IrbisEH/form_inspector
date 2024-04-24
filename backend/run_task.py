import os
import json
from datetime import datetime
from app.Managers.ConfigManager import ConfigManager
from app.Managers.LogManager import LogManager
from app.Managers.DbManager import DbManager, TaskDbModel
from app.Managers.TelegramManager import TelegramManager

from app.Models.TaskConfigModels import TaskModel

DIR = os.path.abspath(os.path.dirname(__file__))
# CREATE_TEST_DATA = True
CREATE_TEST_DATA = False

config_manager = ConfigManager(DIR)
log_manager = LogManager(config_manager)
db_manager = DbManager(config_manager, log_manager)
# telegram_manager = TelegramManager()

if CREATE_TEST_DATA:
    task_data = None

    with open(config_manager.test_data_path, "r") as json_file:
        task_data = json.load(json_file)[0]

    if task_data is None:
        raise Exception("Test data not loaded")

    task_model = TaskModel(**task_data)
    task_model.schedule = json.dumps(task_model.schedule)
    task_model.actions = json.dumps(task_model.actions)

    # db_manager.session.query(TaskModel).all()

    db_manager.session.add(task_model.get_db_model())
    db_manager.session.commit()

    log_manager.debug("Create test row in db")


# GET TASKS

query_result = db_manager.session.query(TaskDbModel).all()

for item in query_result:
    task = TaskModel(**item.__dict__)
    task.convert_props_dic()

    cur_time = datetime.now()
    cur_weekday = str(datetime.now().weekday())

    if cur_weekday not in task.schedule["week_days"]:
        log_manager.info("not today")
        exit()

    for time_string in task.schedule["time"]:
        time_format = "%H:%M"
        schedule_time = datetime.strptime(time_string, time_format).time()
        








# get task list from db
# check time
# if time run task
# get result from task
# send task results






