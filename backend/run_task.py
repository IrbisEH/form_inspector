import os
import json
from app.Managers.ConfigManager import ConfigManager
from app.Managers.LogManager import LogManager
from app.Managers.DbManager import DbManager
from app.Managers.TelegramManager import TelegramManager

from app.Models.TaskConfigModels import TaskModel, TestConfigModel, ScheduleConfigModel

DIR = os.path.abspath(os.path.dirname(__file__))
CREATE_TEST_DATA = True

config_manager = ConfigManager(DIR)
log_manager = LogManager(config_manager)
db_manager = DbManager(config_manager, log_manager)
# telegram_manager = TelegramManager()



if CREATE_TEST_DATA:
    task_data = None

    with open(config_manager.test_data_path, "r") as json_file:
        task_data = json.load(json_file)[0]

    config = TestConfigModel(**task_data)
    schedule = ScheduleConfigModel(
        time_list=["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
        day_week_list=[1, 1, 1, 1, 1, 1, 1]
    )

    task = TaskModel(
        user_id=1,
        enable=1,
        schedule_config=schedule,
        test_config=config,
    )

    print(task.to_dic())

    # task.to_dic




    # model = TaskModel()
    # result = db_manager.get_list(model.db_model)
    # print(result)



# get task list from db
# check time
# if time run task
# get result from task
# send task results






