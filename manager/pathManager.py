import os

class PathManager:


    def __init__(self,pathRoot,appName):
        self.pathRoot=pathRoot
        self.appName=appName

    ########################dir
    # path
    def get_dir_path_root(self):
        return self.pathRoot

    # app dir
    def get_dir_path_app(self):
        return os.path.join(self.get_dir_path_root(), 'app', self.appName)

    # app config.yaml
    def get_dir_path_app_result(self):
        return os.path.join(self.get_dir_path_app(), 'result')

    def get_dir_path_app_tmp(self):
        return os.path.join(self.get_dir_path_app(), 'tmp')


    def get_file_path_app_config(self):
        return os.path.join(self.get_dir_path_app(), 'fi_config.yaml')


    def get_file_path_app_bin(self):
        return os.path.join(self.get_dir_path_app(), self.appName + '.elf')


    def get_file_path_app_objdump(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'objdump.asm')


    def get_file_path_app_objdump_wash(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'objdump_wash.asm')


    def get_file_path_app_trace_inst(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'trace_inst.log')


    def get_file_path_app_trace_inst_wash(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'trace_inst_wash.log')


    def get_file_path_app_trace_golden_result(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'trace_golden_result.log')


    def get_file_path_app_reg_faults(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'reg_faults.txt')


    def get_file_path_app_inst_faults(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'inst_faults.txt')

    def get_file_path_app_mem_faults(self):
        return os.path.join(self.get_dir_path_app_tmp(), 'mem_faults.txt')
