import json
import os
import random
import time

from debugger.GDBServer import JLinkGDBServer
from system.Config import Config
from system.Constant import Constant
from system.Logger import Logger


class Debugger:
    def __init__(self):
        ###gdb server
        self.GDBServer = JLinkGDBServer(log_file=Config.get_file_path_app_gdb_server_log())
        ##init Configuration
        self.trace_inst_log = Config.get_file_path_app_trace_inst()
        self.trace_inst_wash_log = Config.get_file_path_app_trace_inst_wash()
        self.trace_golden_result_log = Config.get_file_path_app_trace_golden_result()
        self.objdump_log = Config.get_file_path_app_objdump_asm()
        self.objdump_wash_log = Config.get_file_path_app_objdump_wash_asm()
        self.objdump_bin = Config.BIN_OBJ_DUMP
        self.elf_bin = Config.get_file_path_app_bin()
        self.total_inst = -1
        self.main_entry_addr = -1
        #####fi info
        self.fi_exec_times = Config.EXEC_TIMES
        self.fi_mode = Config.FAULT_MODE
        self.fi_bfm = Config.FAULT_BFM
        self.fi_regs = Config.FAULT_REGS
        self.fi_reg_width = Config.FAULT_REG_WIDTH
        self.fi_flag_clear_result = Config.FAULT_FLAG_CLEAR_RESULT
        if self.fi_mode == Constant.FAULT_MODE_RF:
            self.fi_file_faults = Config.get_file_path_app_reg_faults()
        else:
            Logger.error('invalid fault mode occurs! fi_mode:{}'.format(self.Config.FAULT_MODE))
            exit(-1)
        pass

    def gen_reg_fault(self, id, regs, bfm, total_inst, reg_width):
        reg = random.sample(regs, 1)
        sec = random.random() * 3
        flips = random.sample(range(reg_width), bfm)
        fault = {
            'id': id,
            'reg': reg,
            'sec': sec,
            'flips': flips,
            'injected': False
        }
        return fault

    def gen_faults(self):
        Logger.debug('Start to generate faults!')
        faults = []
        if self.fi_flag_clear_result or not os.path.exists(self.fi_file_faults):
            Logger.debug('Generate a new faults!')
            for i in range(self.fi_exec_times):
                if self.fi_mode == Constant.FAULT_MODE_RF:
                    fault = self.gen_reg_fault(id=i, regs=self.fi_regs, bfm=self.fi_bfm,
                                               reg_width=self.fi_reg_width, total_inst=self.total_inst)
                    faults.append(fault)
            with open(self.fi_file_faults, 'w') as wf:
                json.dump(faults, wf, indent=Constant.JSON_INDENT)
        else:
            Logger.debug('Faults already have existed!')

    def inject_reg_fault(self, fault):
        pass

    def inject_faults(self):
        Logger.debug('Start to generate faults.')
        fp = self.fi_file_faults
        with open(fp, 'r') as rf:
            faults = json.load(rf)
        for fault in faults:
            if fault['injected']:
                pass
            else:
                if self.fi_mode == Constant.FAULT_MODE_RF:
                    self.inject_reg_fault(fault=fault)
                fault['injected'] = True
            if fault['id'] != 0 and fault['id'] % 50 == 0:
                with open(fp, 'w') as wf:
                    json.dump(faults, wf, indent=Constant.JSON_INDENT)
        with open(fp, 'w') as wf:
            json.dump(faults, wf, indent=Constant.JSON_INDENT)
        pass

    def main(self):
        self.GDBServer.start()
        time.sleep(1)
        if not self.GDBServer.running:
            Logger.error('Errors occur in GDBServer!')
            exit(-1)
        else:
            Logger.debug('GDBServer is running!')
        time.sleep(2)
        self.gen_faults()
        self.inject_faults()
        self.GDBServer.close()



if __name__ == '__main__':
    debugger = Debugger()
    debugger.main()
