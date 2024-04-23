import json
from ..Managers.DbManager import TaskDbModel


class Element:
    def __init__(self, element_type=None, search_type=None, search_value=None, action=None, action_value=None, **kwargs):
        self.element_type = element_type
        self.search_type = search_type
        self.search_value = search_value
        self.action = action
        self.action_value = action_value


class TaskModel:
    def __init__(self, id=None, user_id=None, enable=None, schedule_config=None, test_config=None, created=None, modified=None, **kwargs):
        self.id = id
        self.user_id = user_id
        self.enable = enable
        self.schedule_config = schedule_config
        self.test_config = test_config
        self.created = created
        self.modified = modified
        self.db_model = TaskDbModel

    def to_dic(self):
        dic = vars(self)
        dic["schedule_config"] = self.schedule_config.to_dic()
        dic["test_config"] = self.test_config.get_dic()

    def to_json(self):
        return json.dumps(self.to_dic)


class ScheduleConfigModel:
    def __init__(self, time_list=None, day_week_list=None):
        self.time_list = [] if time_list is None else time_list
        self.day_week_list = [] if day_week_list is None else day_week_list

    def to_dic(self):
        return vars(self)

    def to_json(self):
        return json.dumps(vars(self))


class ActionConfigModel:
    def __init__(self, element_type=None, search_type=None, search_value=None, action=None, action_value=None, **kwargs):
        self.element_type = element_type
        self.search_type = search_type
        self.search_value = search_value
        self.action = action
        self.action_value = action_value


class TestConfigModel:
    def __init__(self, test_id=None, url=None, actions=None):
        self.test_id = test_id
        self.url = url
        self.actions = []

        if actions is not None:
            self.parse(actions)

    def parse(self, actions):
        for action in actions:
            self.actions.append(ActionConfigModel(**action))

    def get_dic(self):
        result = vars(self)
        for item in self.actions:
            result["actions"].append(vars(item))

    def to_json(self):
        return json.dumps(self.get_dic())