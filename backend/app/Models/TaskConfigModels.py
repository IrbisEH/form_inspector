import json
from ..Managers.DbManager import TaskDbModel


class TaskModel:
    def __init__(self, _id=None, user_id=None, enable=None, url=None, schedule=None,
                 actions=None, created=None, modified=None, **kwargs):
        self._id = _id
        self.user_id = user_id
        self.enable = enable
        self.url = url
        self.schedule = schedule
        self.actions = actions
        self.created = created
        self.modified = modified

    def get_db_model(self):
        return TaskDbModel(**self.__dict__)

    def convert_props_dic(self):
        self.schedule = json.loads(self.schedule)
        self.actions = json.loads(self.actions)

    def convert_props_json(self):
        self.schedule = json.dumps(self.schedule)
        self.actions = json.dumps(self.actions)