import json

with open('path_conf.json') as file:
    path_conf = json.load(file)

language = path_conf["language"]
samples = path_conf["samples"]
datasets = path_conf["datasets"]
test_output = path_conf["test_output"]