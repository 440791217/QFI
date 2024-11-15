import os.path
import subprocess

from sympy import false

from logger import Logger
from constant import Constant
from appSys import AppSys
import random
import json


class Emulator:

    def __init__(self, **args):
        Logger.debug("Emulator Init")
        self.trace_inst_log = Constant.get_file_path_app_trace_inst()
        self.trace_inst_wash_log = Constant.get_file_path_app_trace_inst_wash()
        self.trace_golden_result_log = Constant.get_file_path_app_trace_golden_result()
        self.objdump_log = Constant.get_file_path_app_objdump()
        self.objdump_wash_log = Constant.get_file_path_app_objdump_wash()
        self.objdump_bin = Constant.BIN_OBJ_DUMP
        self.elf_bin = Constant.get_file_path_app_bin()
        self.total_inst = -1
        self.main_entry_addr = -1
        #####fi info
        self.fi_exec_times = Constant.EXEC_TIMES
        self.fi_mode = Constant.FAULT_MODE
        self.fi_bfm = Constant.FAULT_BFM
        self.fi_regs = Constant.FAULT_REGS
        self.fi_reg_width = Constant.FAULT_REG_WIDTH
        self.fi_file_reg_faults = Constant.get_file_path_app_reg_faults()
        self.fi_clear_result = Constant.FAULT_CLEAR_RESULT
        pass

    ###########################disassemble
    @staticmethod
    def wash_objdump(objdump_log, objdump_wash_log):
        # filtering comments
        with open(objdump_log, 'r') as rf:
            with open(objdump_wash_log, 'w') as wf:
                ls = rf.readlines()
                for l in ls:
                    if 'file format' in l or 'Disassembly of section' in l:
                        continue
                    elif len(l) == 0:
                        continue
                    elif ';' in l:
                        l = l[0:l.find(';')]
                    l = l.strip()
                    if len(l) == 0:
                        continue
                    wf.write('{}\r\n'.format(l))

    @staticmethod
    def disassemble(objdump_log, objdump_bin, elf_bin):
        with open(objdump_log, 'w') as wf:
            result = subprocess.run([objdump_bin, elf_bin, '-d'], text=True, stdout=wf)
            if result.returncode != 0:
                AppSys.except_with_msg(msg='errors occur in disassemble!')

    ##############################trace inst
    @staticmethod
    def wash_trace_record(trace_inst_log, trace_inst_wash_log,trace_golden_result_log):
        prefix_identify = 'my_qemu_addr:'
        with open(trace_inst_log, 'r') as rf:
            with open(trace_inst_wash_log, 'w') as wf:
                ls = rf.readlines()
                for l in ls:
                    if prefix_identify in l:
                        wf.write(l[len(prefix_identify):l.find(',')])
                        wf.write('\r\n')
            ###collect golden result
            with open(trace_golden_result_log, 'w') as wf:
                for l in ls:
                    l=l.strip()
                    if len(l)>0 and prefix_identify not in l:
                        wf.write(l)
                        wf.write('\r\n')

    @staticmethod
    def gen_trace_record(trace_inst_log, qemu_args):
        ###################trace inst log
        with open(trace_inst_log, 'w') as wf:
            with open(trace_inst_log, 'r') as rf:
                proc = subprocess.Popen(qemu_args, text=True, stdout=wf)
                while True:
                    AppSys.sleep(2)
                    ls = rf.readlines()
                    current = len(ls)
                    Logger.debug('current:{}'.format(current))
                    if current == 0:
                        break  ##the program complete the inst tracing
                if proc.poll() is None:
                    proc.terminate()

    ############################extract_inst
    @staticmethod
    def val_main_entry(objdump_wash_log):
        ##read main function entry addr in .elf file
        with open(objdump_wash_log, 'r') as rf:
            ls = rf.readlines()
            entry_identify = Constant.get_elf_entry_addr_identify()
            for i in range(len(ls)):
                l = ls[i]
                if entry_identify in l:
                    entry_addr = l.split(' ')[0].strip()
                    Logger.debug('main_entry_addr:{}'.format(entry_addr))
                    break
            if entry_addr == -1:
                AppSys.except_with_msg(msg="errors in extract_inst is for entry_identify!")
        entry_addr = int(entry_addr, 16)
        entry_addr = hex(entry_addr)
        return entry_addr

    @staticmethod
    def get_total_inst(trace_inst_wash_log, main_entry_addr):
        with open(trace_inst_wash_log, 'r') as rf:
            ls = rf.readlines()
            total_inst = len(ls)
            for i in range(len(ls)):
                l = ls[i]
                if l.strip() == main_entry_addr:
                    break
                total_inst -= 1
        if total_inst < 1:
            AppSys.except_with_msg(msg='validate main_entry is in failing! total_inst:{}'.format(total_inst))
        Logger.debug('validate main_entry successfully! total_inst:{}'.format(total_inst))
        return total_inst

    @staticmethod
    def gen_reg_fault(id,regs, bfm, total_inst,reg_width):
        reg = random.sample(regs, 1)
        inst = random.randint(0, total_inst - 1)
        flips = random.sample(range(reg_width), bfm)
        fault = {
            'id': id,
            'reg': reg,
            'inst': inst,
            'flips': flips,
            'injected': False
        }
        return fault

    @staticmethod
    def gen_inst_fault():
        pass

    @staticmethod
    def gen_mem_fault():
        pass

    @staticmethod
    def inject_faults(self):
        pass

    def extract_inst(self):
        AppSys.except_if_not_exists(fp=self.objdump_wash_log, msg='errors in extract_inst is for objdump_wash_log!')
        AppSys.except_if_not_exists(fp=self.trace_inst_wash_log, msg='errors in extract_inst is for trace_inst_log!')
        self.main_entry_addr = Emulator.val_main_entry(objdump_wash_log=self.objdump_wash_log)
        self.total_inst = self.get_total_inst(trace_inst_wash_log=self.trace_inst_wash_log,
                                              main_entry_addr=self.main_entry_addr)

    def gen_faults(self):
        faults = []
        if self.fi_exec_times < 1:
            AppSys.except_with_msg('fi_exec_times<1!')
        if self.fi_mode == Constant.FAULT_MODE_RF:
            fp = self.fi_file_reg_faults
            # Emulator.gen_reg_faults(fp=self.fi_file_reg_faults,
            #                         fi_regs=self.fi_regs,fi_bfm=self.fi_bfm,fi_exec_times=self.fi_exec_times)
        else:
            AppSys.except_with_msg(msg='invalid fault mode occurs! fi_mode:{}'.format(self.fi_mode))
        if self.fi_clear_result or os.path.exists(fp) is False:
            for i in range(self.fi_exec_times):
                if self.fi_mode == Constant.FAULT_MODE_RF:
                    fault=Emulator.gen_reg_fault(id=i,regs=self.fi_regs,bfm=self.fi_bfm,
                                                 reg_width=self.fi_reg_width,total_inst=self.total_inst)
                    faults.append(fault)
            with open(fp, 'w') as wf:
                json.dump(faults, wf, indent=1)
        return fp



    def main(self):
        # Emulator.disassemble(objdump_log=self.objdump_log, objdump_bin=self.objdump_bin, elf_bin=self.elf_bin)
        # Emulator.wash_objdump(objdump_log=self.objdump_log, objdump_wash_log=self.objdump_wash_log)

        # Emulator.gen_trace_record(trace_inst_log=self.trace_inst_log, qemu_args=Constant.get_qemu_trace_inst_args())
        Emulator.wash_trace_record(trace_inst_log=self.trace_inst_log, trace_inst_wash_log=self.trace_inst_wash_log,
                                   trace_golden_result_log=self.trace_golden_result_log)  ##################wash log

        self.extract_inst()
        self.gen_faults()
        pass


if __name__ == '__main__':
    emulator = Emulator()
    emulator.main()
