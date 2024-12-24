import json
import os
import random
import time

from debugger.GDB import GDB
from debugger.GDBServer import GDBServer
from system.Config import Config
from system.Constant import Constant
from system.Logger import Logger


def update_faults(fpath, faults):
    with open(fpath, 'w') as wf:
        json.dump(faults, wf, indent=2)


def load_faults(fpath):
    with open(fpath, 'r') as rf:
        faults = json.load(rf)
    return faults


def gen_reg_faults(exec_times, regs, bfm, reg_width):
    faults = []
    for i in range(exec_times):
        before_tm = random.random() * 3
        regs = random.sample(regs, 1)
        fault = {
            'id': i,
            'regs': [],
            'before_tm': before_tm,
            'flips': [],
            'injected': False
        }
        for reg in regs:
            flips = random.sample(range(reg_width), bfm)
            obj={
                'name':reg,
                'flips': flips,
                'before_value': -1,
                'after_value': -1,
            }
            fault['regs'].append(obj)
        faults.append(fault)
    return faults

# def inject_reg_fault(fault):

def inject_fault_once(mode=None, fault=None):
    if mode == Constant.FAULT_MODE_RF:
        gdb = GDB()
        gdb.set_elf_bin('/home/mark/data/PycharmProjects/QFI/app/stm32f407_test/stm32f407_test.elf')
        gdb.set_gdb_bin('arm-none-eabi-gdb')
        gdb.set_fault(fault)
        gdb.start()
        gdb.join()
        pass
    else:
        assert mode == 'Invalid Fault Mode.'
    fault['injected'] = True
    return fault


class Debugger:
    def __init__(self):
        ###gdb server
        self.gdb_server = None
        ##init Configuration
        self.trace_inst_log = None
        self.trace_inst_wash_log = None
        self.trace_golden_result_log = None
        self.objdump_log = None
        self.objdump_wash_log = None
        self.objdump_bin = None
        self.elf_bin = None
        self.total_inst = None
        self.main_entry_addr = None
        #####fi info
        self.fi_exec_times = None
        self.fi_mode = None
        self.fi_bfm = None
        self.fi_regs = None
        self.fi_reg_width = None
        self.fi_flag_clear_result = None
        pass

    def init(self):
        ###gdb server
        ###gdb server
        self.gdb_server = None
        # self.gdb_server = GDBServer()
        # self.gdb_server.set_command(
        #     'JLinkGDBServer -port 2331 -device STM32F407ZG -endian little -speed 4000 -if swd -vd -nogui'.split())
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

    def check_gdb_server(self):
        assert self.gdb_server.running
        assert self.gdb_server.proc
        assert self.gdb_server.returncode == 0

    def gen_faults(self):
        if self.fi_mode == Constant.FAULT_MODE_RF:
            faults = gen_reg_faults(exec_times=self.fi_exec_times, regs=self.fi_regs, bfm=self.fi_bfm,
                                    reg_width=self.fi_reg_width)
        else:
            assert self.fi_mode == 'Invalid mode'
        with open(self.fi_file_faults, 'w') as wf:
            json.dump(faults, wf, indent=2)

    def do_inject_fault_once(self, mode=None, fault=None):

        pass

    def inject_faults(self):
        fpath = self.fi_file_faults
        faults = load_faults(fpath=self.fi_file_faults)
        log_file_dir = os.path.join(Config.get_dir_path_app_result(), self.fi_mode, '{}'.format(self.fi_bfm))
        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)
        for fault in faults:
            log_file_name='{:04d}.txt'.format(fault['id'])
            log_file_path=os.path.join(log_file_dir,log_file_name)
            if not fault['injected']:
                fault['log_file_path']=log_file_path
                # check gdbserver
                self.check_gdb_server()
                # inject fault
                fault = inject_fault_once(mode=self.fi_mode, fault=fault)
            if fault['id'] != 0 and fault['id'] % 50 == 0:
                update_faults(fpath=fpath, faults=faults)
        update_faults(fpath=fpath, faults=faults)

    def main(self):
        if self.fi_flag_clear_result or not os.path.exists(self.fi_file_faults):
            self.gen_faults()
            Logger.debug('Generate faults.')
        else:
            Logger.debug('Read existed faults.')
        self.gdb_server = GDBServer()
        self.gdb_server.set_command(
            'JLinkGDBServer -port 2331 -device STM32F407ZG -endian little -speed 4000 -if swd -vd -nogui'.split())
        self.gdb_server.start()
        Logger.debug('Start gdb_server.')
        time.sleep(1)
        Logger.debug('Start to inject faults.')
        self.inject_faults()
        self.gdb_server.close()
        Logger.debug('Close gdb_server. The returncode of gdb_server is {}.'.format(self.gdb_server.returncode))


if __name__ == '__main__':
    debugger = Debugger()
    debugger.init()
    debugger.main()
