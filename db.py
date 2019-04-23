import os
import configparser

CONFIG_FILE="config.ini"

def get_config(section):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), CONFIG_FILE))
    return dict(config[section])