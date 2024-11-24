import os.path

from aiohttp.web_routedef import static

from system.Logger import Logger
from system.Config import Config
import yaml

##manager
from manager.pathManager import PathManager
from system.Utils import Utils


class AppSys:

    Params = None
    Logger = None


    #####################get misinject_faultsc
    @staticmethod
    def get_qemu_trace_inst_args():
        cmd = AppSys.config.BIN_QEMU_LAUNCHER
        machine = AppSys.config.QEMU_BOARD
        kernel = AppSys.config.get_file_path_app_bin()
        plugin = '/home/mark/data/qemu/build/contrib/plugins/libinst_profile.so'
        data = [cmd, '-M', machine,
                '-kernel', kernel, '--plugin', plugin, '-d', 'plugin', '-nographic','-serial','stdio','-monitor', 'null']
        return data

    @staticmethod
    def get_elf_entry_addr_identify():
        return '<main>:'


#################################################init


    def init_config(self):
        fp = self.pm.get_file_path_app_config()
        if os.path.exists(fp):
            data = self.utils.load_by_json(fp)
        else:
            binPath = self.pm.get_file_path_app_bin()
            binObjDump = self.config.BIN_OBJ_DUMP
            data = {
                'fault': {
                    'bfm': self.config.FAULT_BFM,
                    'mode': self.config.FAULT_MODE,
                },
                'exe_times': self.config.EXEC_TIMES,
                'binPath': binPath,
                'binObjDump': binObjDump,
            }
            data = self.utils.dump_by_json(fp,data )
        return data


    def init_dirs(self):
        dirs = [
            [self.pm.get_dir_path_app_result(), 'PATH_APP_RESULT'],
            [self.pm.get_dir_path_app_tmp(), 'PATH_APP_TMP'],
        ]
        for dd in dirs:
            if os.path.exists(dd[0]) is False:
                os.makedirs(dd[0])
            self.logger.debug('{}=>{}'.format(dd[1], dd[0]))




    def __init__(self):
        #init library and viable
        self.logger=Logger()
        self.utils=Utils(logger=self.logger)
        self.config=Config(utils=self.utils)
        self.pm=PathManager(pathRoot=self.config.PATH_ROOT,appName=self.config.APP_NAME)
        ################init system
        self.init_dirs()
        data=self.init_config()
if __name__ == '__main__':
    pass