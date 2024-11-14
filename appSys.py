import os.path
import time
from logger import Logger
from constant import Constant
import yaml

class AppSys:

    #app config.yaml
    @staticmethod
    def get_app_config():
        with open(Constant.get_file_path_app_config(), 'r') as rf:
            data=yaml.safe_load(rf)
        return data

    @staticmethod
    def sleep(tm=1):
        time.sleep(tm)
        Logger.debug('sleep in {} sec!'.format(tm))


if __name__ == '__main__':
    pass