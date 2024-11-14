import yaml
import os

from constant import Constant
from logger import Logger


def init_dirs():
    dirs=[
        [Constant.get_dir_path_app_result(), 'PATH_APP_RESULT'],
    ]
    for dir in dirs:
        if os.path.exists(dir[0]) is False:
            os.makedirs(dir[0])
        Logger.debug('{}=>{}'.format(dir[1],dir[0]))
    pass

def init_config():
    fp=Constant.get_file_path_app_config()
    if os.path.exists(fp):
        with open(fp,'r') as rf:
            data=yaml.safe_load(rf)
    else:
        with open(fp,'w',encoding="utf-8") as wf:
            #binPath
            binPath=Constant.get_file_path_app_bin()
            binObjDump=Constant.BIN_OBJ_DUMP
            data={
                'fault':{
                    'bfm':Constant.FAULT_BFM_SINGLE,
                    'mode':Constant.FAULT_MODE_RF,
                },
                'exe_times':Constant.EXEC_TIMES,
                'binPath':binPath,
                'binObjDump':binObjDump,
            }
            yaml.dump(data,wf)
    return data

def init_tmp():
    fp=Constant.get_dir_path_app_tmp()
    if os.path.exists(fp) is False:
        os.makedirs(fp)

def init_result():
    pass

def init_exec():
    pass

def init(**args):

    ##########init dir
    init_dirs()
    ##########init config
    data=init_config()
    ##########init result
    init_result()
    ##########init exec
    init_exec()
    ##########init tmp
    init_tmp()
    return data

if __name__ == '__main__':
    init()

