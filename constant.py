import os
#user attribute
APP_NAME='stm32f100_mk'


PATH_ROOT=os.getcwd()

#path
def GET_PATH_ROOT():
    return PATH_ROOT

#app dir
def GET_PATH_APP():
    return os.path.join(GET_PATH_ROOT(),'app',APP_NAME)

def GET_PATH_APP_CONFIG():
    return os.path.join(GET_PATH_APP(),'config')

#app config.yaml

def GET_PATH_APP_RESULT():
    return os.path.join(GET_PATH_APP(),'result')

def GET_PATH_APP_EXEC():
    return os.path.join(GET_PATH_APP(),'exec')


#files dir
def GET_PATH_FILES():
    return os.path.join(GET_PATH_ROOT(),'files')

def GET_PATH_FILES_EXEC():
    return os.path.join(GET_PATH_FILES(),'exec')

def PATH_FILES_TMP():
    return os.path.join(GET_PATH_FILES(),'tmp')



#fault bfm
FAULT_BFM_SINGLE='single_bit'

#fault mode
FAULT_MODE_RF='register_file'

#bin
BIN_OBJ_DUMP="arm-none-eabi-objdump"



###user attribute
FAULT_MODE=FAULT_MODE_RF
FAULT_BFM=FAULT_BFM_SINGLE
EXEC_TIMES=1000
FLAG_CLEAG_RESULT=False

if __name__=='__main__':
    print("PATH_ROOT:{}".format(PATH_ROOT))



