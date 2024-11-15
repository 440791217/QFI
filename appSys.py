import json
import os.path
import time
import shutil
from logger import Logger
from params import Params
import yaml

class AppSys:

    Params = None

    @staticmethod
    def debug(msg):
        Logger.debug(msg)

    @staticmethod
    def info(msg):
        Logger.info(msg)

    @staticmethod
    def warning(msg):
        Logger.warning(msg)

    @staticmethod
    def error(msg):
        Logger.error(msg)

    @staticmethod
    def critical(msg):
        Logger.critical(msg)

    #app config.yaml
    @staticmethod
    def get_app_config():
        with open(Params.get_file_path_app_config(), 'r') as rf:
            data=yaml.safe_load(rf)
        return data

    @staticmethod
    def sleep(tm=1):
        time.sleep(tm)
        AppSys.debug('sleep in {} sec!'.format(tm))

    @staticmethod
    def delete_by_path(fp):
        if os.path.exists(fp):
            shutil.rmtree(fp)
            AppSys.debug('delete path:{}'.format(fp))
        else:
            AppSys.debug('path does not exist:{}'.format(fp))

    @staticmethod
    def except_with_msg(code=-1,msg=None):
        if msg is not None:
            AppSys.error(msg)
        exit(code)

    @staticmethod
    def except_if_not_exists(fp,msg=None):
        if os.path.exists(fp) is False:
            if msg is not None:
                AppSys.error(msg)
                AppSys.error(msg)
            exit(-1)


#################################################init
    @staticmethod
    def init_dirs():
        dirs = [
            [Params.get_dir_path_app_result(), 'PATH_APP_RESULT'],
            [Params.get_dir_path_app_tmp(), 'PATH_APP_TMP'],
        ]
        for dir in dirs:
            if os.path.exists(dir[0]) is False:
                os.makedirs(dir[0])
            AppSys.debug('{}=>{}'.format(dir[1], dir[0]))

    @staticmethod
    def init_config():
        fp = Params.get_file_path_app_config()
        if os.path.exists(fp):
            with open(fp, 'r') as rf:
                data = yaml.safe_load(rf)
        else:
            with open(fp, 'w', encoding="utf-8") as wf:
                # binPath
                binPath = Params.get_file_path_app_bin()
                binObjDump = Params.BIN_OBJ_DUMP
                data = {
                    'fault': {
                        'bfm': Params.FAULT_BFM_1,
                        'mode': Params.FAULT_MODE_RF,
                    },
                    'exe_times': Params.EXEC_TIMES,
                    'binPath': binPath,
                    'binObjDump': binObjDump,
                }
                yaml.dump(data, wf)
        return data

    @staticmethod
    def init_sys():
        AppSys.init_dirs()
        AppSys.init_config()

###########################################json
    @staticmethod
    def dump_by_json(fp,data):
        with open(fp,'w') as wf:
            json.dump(data,wf,indent=2)

    @staticmethod
    def load_by_json(fp):
        with open(fp,'r') as rf:
            data=json.load(rf)
        return data

AppSys.Params=Params

if __name__ == '__main__':
    pass