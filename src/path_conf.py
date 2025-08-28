import json
import logging
import os
from os import path


language = path.join(os.getcwd(), "resources", "languages")
samples = path.join(os.getcwd(), "resources", "samples")
test_output = path.join(os.getcwd(), "tests", "output")

try:
    with open('path_conf.json') as file:
        path_conf = json.load(file)
    datasets = path_conf["datasets"]
    if not path.isdir(datasets):
        datasets = None
except Exception as error:
    datasets = None
if not datasets:
    logging.getLogger(__name__).error("datasets path IS EMPTY")
