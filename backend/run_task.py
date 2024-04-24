import os
import json

from datetime import datetime, timedelta

from app.Managers.ConfigManager import ConfigManager
from app.Managers.LogManager import LogManager
from app.Managers.DbManager import DbManager, TaskDbModel
from app.Managers.TelegramManager import TelegramManager

from app.Models.TaskConfigModels import TaskModel


DIR = os.path.abspath(os.path.dirname(__file__))
CREATE_TEST_DATA = False


def write_to_db_test_data(json_data_file, log):
    try:
        data = None

        with open(json_data_file, "r") as file:
            data = json.load(file)[0]

        if data is None:
            raise Exception("Error! can not load test data.")

        model = TaskModel(**data)
        model.schedule = json.dumps(model.schedule)
        model.actions = json.dumps(model.actions)

        db.session.add(model.get_db_model())
        db.session.commit()

        log.debug("Create test row in db")

    except Exception as e:
        log.error(e)
        exit()

def is_time_to_start(schedule, log):

    result = False
    time_format = "%H:%M"

    try:
        cur_time = datetime.now().time()
        cur_weekday = str(datetime.now().weekday())

        if cur_weekday in schedule["week_days"]:
            for time_string in schedule["time"]:

                start_period = (datetime.strptime(time_string, time_format) - timedelta(minutes=5)).time()
                end_period = (datetime.strptime(time_string, time_format) + timedelta(minutes=5)).time()

                if start_period < cur_time <= end_period:
                    result = True

    except Exception as e:
        log.error(e)
        exit()

    return result


if __name__ == "__main__":
    try:
        config = ConfigManager(DIR)
        log = LogManager(config)
        db = DbManager(config, log)
        # telegram = TelegramManager()

        # WRITE TEST DATA TO DB IF NEED
        if CREATE_TEST_DATA:
            write_to_db_test_data(config.test_data_path, log)

        query_result = db.session.query(TaskDbModel).all()

        if len(query_result) == 0:
            log.warning("Not found any tasks in database.")

        for item in query_result:
            task = TaskModel(**item.__dict__)
            task.convert_props_dic()

            if not is_time_to_start(task.schedule, log):
                continue

            print("start task")

        # get task list from db
        # check time
        # if time run task
        # get result from task
        # send task results

    except Exception as e:
        log.error(e)
        exit()

