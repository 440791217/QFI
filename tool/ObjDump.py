import subprocess
import json
from textwrap import indent

from system.Config import Config
from system.Logger import Logger

class ObjDump:

    def __init__(self):
        pass

    @staticmethod
    def genFunc(l=None):
        assert (l)
        Name = l[l.find('<') + 1:l.find('>')].strip().strip('\n')
        Inst = []
        func = {
            'Name': Name,
            'Inst': Inst
        }
        return func

    @staticmethod
    def genInst(l=None):
        assert (l)
        info = l[0:-1]
        addr = info[:7]
        opcode = info[8:18].replace('\t', '').replace(' ', '')
        t = info[19:].strip().replace('\t', ' ')
        f = t.find(' ')
        if f > 0:
            opname = t[:f]
            operator = t[f:]
        else:
            opname = t
            operator = 'null'
        instInfo = {
            'addr': addr,
            'opcode': opcode,
            'opname': opname,
            'operator': operator
        }
        return instInfo


    @staticmethod
    def divFuncInst(objdump_wash_log,objdump_wash_log1):
        func_list = []
        with open(objdump_wash_log,'r') as rf:
            lines=rf.readlines()
            for l in lines:
                if '>:' in l and '<' in l:
                    func=ObjDump.genFunc(l=l)
                    func_list.append(func)
                elif l.find(':')==7:
                    assert (func is not None)
                    instInfo=ObjDump.genInst(l=l)
                    func['Inst'].append(instInfo)
                    # print(info)
                    # print('addr:{},opcode:{},opname:{},operatos:{}'.format(addr,opcode,opname,operator))
        # Logger.debug(func_list)
        with open(objdump_wash_log1,'w') as wf:
            json.dump(func_list,wf,indent=2)



    @staticmethod
    def disassemble(objdump_log, objdump_bin, elf_bin):
        with open(objdump_log, 'w') as wf:
            result = subprocess.run([objdump_bin, elf_bin, '-d'], text=True, stdout=wf)
        return result.returncode

    @staticmethod
    def do_clear(l):
        l = l.strip()  # clear trash symbol
        if 'file format' in l or 'Disassembly of section' in l:
            l = ''
        elif len(l) == 0:
            l = ''
        elif ':' not in l:
            l = ''
        if ';' in l:
            l = l[:l.find(';')]
        if '<' in l and '>' in l and ('>:' not in l):
            l = l[:l.find('<')]
        l = l.strip()
        return l

    @staticmethod
    def wash_objdump(objdump_log, objdump_wash_log):
        # filtering comments
        with open(objdump_log, 'r') as rf:
            with open(objdump_wash_log, 'w') as wf:
                ls = rf.readlines()
                for l in ls:
                    l = ObjDump.do_clear(l=l)
                    if len(l) == 0:
                        continue
                    wf.write('{}\r\n'.format(l))

    # @staticmethod
    # def parse_main(objdump_wash_log1=None):
    #     assert (objdump_wash_log1)
    #     with open(objdump_wash_log1,'r') as rf:
    #         data=json.load(rf)



if __name__ == '__main__':
    ret = ObjDump.disassemble(objdump_log=Config.get_file_path_app_objdump_asm(),
                              objdump_bin=Config.BIN_OBJ_DUMP,
                              elf_bin=Config.get_file_path_app_bin())
    assert (ret == 0)
    ObjDump.wash_objdump(objdump_log=Config.get_file_path_app_objdump_asm(),
                         objdump_wash_log=Config.get_file_path_app_objdump_wash_asm())

    ObjDump.divFuncInst(objdump_wash_log=Config.get_file_path_app_objdump_wash_asm(),
                        objdump_wash_log1=Config.get_file_path_app_objdump_wash_json())