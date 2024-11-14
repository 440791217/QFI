import yaml
import os
import logger as logger
import constant as constant


def init_dirs():
    dirs=[
        [constant.GET_PATH_APP_CONFIG(),'PATH_APP_CONFIG'],
        [constant.GET_PATH_APP_RESULT(),'PATH_APP_RESULT'],
        [constant.GET_PATH_APP_EXEC(),'PATH_APP_EXEC']
    ]
    for dir in dirs:
        if os.path.exists(dir[0]) is False:
            os.makedirs(dir[0])
        logger.debug('{}=>{}'.format(dir[1],dir[0]))  
    pass

def init_config():
    fp=os.path.join(constant.GET_PATH_APP_CONFIG(),'config.yaml')
    if os.path.exists(fp):
        with open(fp,'r') as rf:
            data=yaml.safe_load(rf)
    else:
        with open(fp,'w',encoding="utf-8") as wf:
            #binPath
            binPath=os.path.join(constant.GET_PATH_APP_EXEC(),constant.APP_NAME+'.elf')
            binObjDump=constant.BIN_OBJ_DUMP
            data={
                'fault':{
                    'bfm':constant.FAULT_BFM_SINGLE,
                    'mode':constant.FAULT_MODE_RF,
                },
                'exe_times':constant.EXEC_TIMES,
                'binPath':binPath,
                'binObjDump':binObjDump,
            }
            yaml.dump(data,wf)
    return data

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
    return data

if __name__ == '__main__':
    init()

