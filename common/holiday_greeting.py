import os
from configparser import ConfigParser


def get_greeting():
    if __name__ == '__main__':
        module_path = ''
    else:
        module_path = os.path.dirname(__file__) + '/'
    cfg = 'config.ini'
    config = ConfigParser()
    config.read(module_path + cfg)
    return config['customization']['holiday_greeting']


holiday_greeting = get_greeting()
