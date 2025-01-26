import os.path
import json

from debugger.Debugger import Debugger
from system.Constant import Constant
##manager
from system.Config import Config
from system.Logger import Logger


class AppSys:
    # #####################get misinject_faultsc
    # @staticmethod
    # def get_qemu_trace_inst_args():
    #     cmd = AppSys.config.BIN_QEMU_LAUNCHER
    #     machine = AppSys.config.QEMU_BOARD
    #     kernel = AppSys.config.get_file_path_app_bin()
    #     plugin = '/home/mark/data/qemu/build/contrib/plugins/libinst_profile.so'
    #     data = [cmd, '-M', machine,
    #             '-kernel', kernel, '--plugin', plugin, '-d', 'plugin', '-nographic', '-serial', 'stdio', '-monitor',
    #             'null']
    #     return data
    #
    # @staticmethod
    # def get_elf_entry_addr_identify():
    #     return '<main>:'

    #################################################init
    @staticmethod
    def init_dirs():
        dirs = [
            [Config.get_dir_path_app_result(), 'PATH_APP_RESULT'],
            [Config.get_dir_path_app_tmp(), 'PATH_APP_TMP'],
        ]
        for dd in dirs:
            if os.path.exists(dd[0]) is False:
                os.makedirs(dd[0])
            Logger.debug('{}=>{}'.format(dd[1], dd[0]))

    @staticmethod
    def read_config():
        fp = Config.get_file_path_app_config()
        if os.path.exists(fp):
            with open(fp, 'r') as rf:
                data = json.load(rf)
        else:
            data = {
                Constant.KEY_APP_NAME:Config.APP_NAME,
                Constant.KEY_FAULT_BFM: Config.FAULT_BFM,
                Constant.KEY_FAULT_MODE:Config.FAULT_MODE,
                Constant.KEY_FAULT_EXE_TIMES:Config.EXEC_TIMES
            }
            with open(fp, 'w') as wf:
                json.dump(data, wf, indent=Constant.JSON_INDENT)
        return data

    def main(self):
        # self.debugger.main()
        pass

    def __init__(self):
        ################init system
        AppSys.init_dirs()
        # init library and viable
        data = AppSys.read_config()

        # self.debugger=Debugger(config=self.config,logger=self.logger,utils=self.utils,pm=self.pm)


if __name__ == '__main__':
    appSys=AppSys()
    debugger = Debugger()
    debugger.init()
    debugger.main()
    pass
