import os
import system.Constant as Constant


class Config:
    ######predefine start
    # qemu parameter
    QEMU_BOARD = 'stm32vldiscovery'
    #######predefine end

    # user attribute start
    APP_NAME = 'stm32f100_mk'
    PATH_ROOT = os.getcwd()
    ###user attribute
    FAULT_MODE = Constant.FAULT_MODE_RF
    FAULT_BFM = Constant.FAULT_BFM_1
    EXEC_TIMES = 1000
    FAULT_RESET_ALL =False
    FAULT_CLEAR_RESULT = False
    BIN_OBJ_DUMP = 'arm-none-eabi-objdump'
    BIN_QEMU_LAUNCHER = 'qemu-system-arm'
    FAULT_REGS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r11', 'r12', 'sp', 'lr', 'pc']
    FAULT_REG_WIDTH = 32

    # user attribute end

    def __init__(self,utils):
        self.utils=utils
        pass


if __name__ == '__main__':
    pass
    # print("PATH_ROOT:{}".format(config.PATH_ROOT))
    # print("FAULT_MODE:{}".format(Params.FAULT_MODE))
    # print("file path app config:{}".format(Params.get_file_path_app_config()))
