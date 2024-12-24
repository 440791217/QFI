import os

from system.Constant import Constant


class Config:
    ######predefine start
    # qemu parameter
    QEMU_BOARD = 'stm32vldiscovery'
    #######predefine end

    # user attribute start
    APP_NAME = 'stm32F407_mk'
    PATH_ROOT = '/home/mark/data/PycharmProjects/QFI' #os.getcwd()
    ###user attribute
    FAULT_MODE = Constant.FAULT_MODE_RF
    FAULT_BFM = Constant.FAULT_BFM_1
    EXEC_TIMES = 1000
    FAULT_RESET_ALL = False
    FAULT_FLAG_CLEAR_RESULT = True
    BIN_OBJ_DUMP = 'arm-none-eabi-objdump'
    BIN_QEMU_LAUNCHER = 'qemu-system-arm'
    FAULT_REGS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r11', 'r12', 'sp', 'lr', 'pc']
    FAULT_REG_WIDTH = 32

    @staticmethod
    def get_dir_path_root():
        return Config.PATH_ROOT

    # app dir
    @staticmethod
    def get_dir_path_app():
        return os.path.join(Config.get_dir_path_root(), 'app', Config.APP_NAME)

    # app config
    @staticmethod
    def get_dir_path_app_result():
        return os.path.join(Config.get_dir_path_app(), 'result')

    @staticmethod
    def get_dir_path_app_tmp():
        return os.path.join(Config.get_dir_path_app(), 'tmp')

    @staticmethod
    def get_file_path_app_config():
        return os.path.join(Config.get_dir_path_app(), 'fi_config.json')

    @staticmethod
    def get_file_path_app_bin():
        return os.path.join(Config.get_dir_path_app(), Config.APP_NAME + '.elf')

    @staticmethod
    def get_file_path_app_objdump_asm():
        return os.path.join(Config.get_dir_path_app_tmp(), 'objdump.asm')

    @staticmethod
    def get_file_path_app_objdump_wash_asm():
        return os.path.join(Config.get_dir_path_app_tmp(), 'objdump_wash.asm')

    @staticmethod
    def get_file_path_app_objdump_wash_json():
        return os.path.join(Config.get_dir_path_app_tmp(), 'objdump_wash.json')

    @staticmethod
    def get_file_path_app_trace_inst():
        return os.path.join(Config.get_dir_path_app_tmp(), 'trace_inst.log')

    @staticmethod
    def get_file_path_app_trace_inst_wash():
        return os.path.join(Config.get_dir_path_app_tmp(), 'trace_inst_wash.log')

    @staticmethod
    def get_file_path_app_trace_golden_result():
        return os.path.join(Config.get_dir_path_app_tmp(), 'trace_golden_result.log')

    @staticmethod
    def get_file_path_app_gdb_server_log():
        return os.path.join(Config.get_dir_path_app_tmp(), 'gdb_server.log')

    @staticmethod
    def get_file_path_app_reg_faults():
        return os.path.join(Config.get_dir_path_app_tmp(), 'reg_faults.txt')

    @staticmethod
    def get_file_path_app_inst_faults():
        return os.path.join(Config.get_dir_path_app_tmp(), 'inst_faults.txt')

    @staticmethod
    def get_file_path_app_mem_faults():
        return os.path.join(Config.get_dir_path_app_tmp(), 'mem_faults.txt')


if __name__ == '__main__':
    pass
    # print("PATH_ROOT:{}".format(config.PATH_ROOT))
    # print("FAULT_MODE:{}".format(Params.FAULT_MODE))
    # print("file path app config:{}".format(Params.get_file_path_app_config()))
