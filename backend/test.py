import json
from app.Managers.InspectManager import InspectManager
from app.Models.TaskConfigModels import Element

CONFIG_PATH = "data/test_config_3.json"

test_config = None
actions = []

with open(CONFIG_PATH, "r") as json_file:
    test_config = json.load(json_file)[0]

if test_config is None or "actions" not in test_config:
    raise Exception("Test config not loaded")

for item in test_config["actions"]:
    actions.append(Element(**item))

inspector = InspectManager(
    headless=False,
    url=test_config["url"],
    actions=actions
)

inspector.start()

