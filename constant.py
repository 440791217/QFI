import os

class Constant:

    ######predefine start
    # fault bfm
    FAULT_BFM_SINGLE = 'single_bit'
    # fault mode
    FAULT_MODE_RF = 'register_file'
    # bin
    BIN_OBJ_DUMP = 'arm-none-eabi-objdump'
    BIN_QEMU_LAUNCHER='qemu-system-arm'
    #qemu parameter
    QEMU_BOARD='stm32vldiscovery'
    #######predefine end

    #user attribute start
    APP_NAME='stm32f100_mk'
    PATH_ROOT=os.getcwd()
    ###user attribute
    FAULT_MODE = FAULT_MODE_RF
    FAULT_BFM = FAULT_BFM_SINGLE
    EXEC_TIMES = 1000
    FLAG_CLEAR_RESULT = False
    #user attribute end

########################dir
    #path
    @staticmethod
    def get_dir_path_root():
        return Constant.PATH_ROOT

    #app dir
    @staticmethod
    def get_dir_path_app():
        return os.path.join(Constant.get_dir_path_root(), 'app', Constant.APP_NAME)

    #app config.yaml
    @staticmethod
    def get_dir_path_app_result():
        return os.path.join(Constant.get_dir_path_app(), 'result')

    @staticmethod
    def get_dir_path_app_tmp():
        return os.path.join(Constant.get_dir_path_app(), 'tmp')


#####################file        QEMU_TRACE_INST_ARGS = '-M {} -monitor null -kernel'
    @staticmethod
    def get_file_path_app_config():
        return os.path.join(Constant.get_dir_path_app(),'fi_config.yaml')

    @staticmethod
    def get_file_path_app_bin():
        return os.path.join(Constant.get_dir_path_app(),Constant.APP_NAME+'.elf')

    @staticmethod
    def get_file_path_app_objdump():
        return os.path.join(Constant.get_dir_path_app_tmp(), 'objdump.asm')

    @staticmethod
    def get_file_path_app_objdump_wash():
        return os.path.join(Constant.get_dir_path_app_tmp(), 'objdump_wash.asm')

    @staticmethod
    def get_file_path_app_trace_inst():
        return os.path.join(Constant.get_dir_path_app_tmp(), 'trace_inst.log')

    @staticmethod
    def get_file_path_app_trace_inst_wash():
        return os.path.join(Constant.get_dir_path_app_tmp(), 'trace_inst_wash.log')

#####################get misc
    @staticmethod
    def get_qemu_trace_inst_args():
        cmd=Constant.BIN_QEMU_LAUNCHER
        machine=Constant.QEMU_BOARD
        kernel=Constant.get_file_path_app_bin()
        plugin='/home/mark/data/qemu/build/contrib/plugins/libinst_profile.so'
        data=[cmd,'-M',machine,
              '-kernel',kernel,'--plugin',plugin,'-d', 'plugin','-nographic']
        return data


if __name__=='__main__':
    print("PATH_ROOT:{}".format(Constant.PATH_ROOT))
    print("FAULT_MODE:{}".format(Constant.FAULT_MODE))
    print("file path app config:{}".format(Constant.get_file_path_app_config()))



