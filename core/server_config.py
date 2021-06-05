import json
import os.path


config_path = open(os.path.dirname(__file__) + r"/../server_config.json")
server_config: dict = json.load(config_path)
