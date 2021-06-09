import os
import shutil
import configparser

from exceptions import ChallengeBotException

class Config:
    
    def __init__(self, config_file):
        self.config_file = config_file
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        self.command_prefix = config.get('Chat', 'CommandPrefix', fallback=ConfigDefaults.command_prefix)

class ConfigDefaults:

    command_prefix = 'bb!'

    options_file = 'config/options.ini'