import subprocess
import yaml
from constant import Constant
class Disas:

    # bin=>asm
    @staticmethod
    def disassemble(**args):
        fp = Constant.get_file_path_app_objdump()
        objdump = Constant.BIN_OBJ_DUMP
        elf_bin = Constant.get_file_path_app_bin()
        with open(fp, 'w') as wf:
            result = subprocess.run([objdump, elf_bin, '-d'], text=True, stdout=wf)
            if result.returncode != 0:
                print("errors occur in disassemble!\n")
                exit(-1)

    # filtering comments
    @staticmethod
    def wash_objdump(**args):
        fp = Constant.get_file_path_app_objdump()
        wash_fp = Constant.get_file_path_app_objdump_wash()
        rf=open(fp, 'r')
        wf=open(wash_fp, 'w')
        ls=rf.readlines()
        for l in ls:
            if 'file format' in l or 'Disassembly of section' in l:
                continue
            elif len(l)==0:
                continue
            elif ';' in l:
                l=l[0:l.find(';')]
            l = l.strip()
            if len(l)==0:
                continue
            wf.write('{}\r\n'.format(l))
        rf.close()
        wf.close()
    @staticmethod
    def main():
        Disas.disassemble()
        Disas.wash_objdump()


if __name__ == '__main__':
    Disas.main()
    # disassemble(pathBin=PATH_BIN)
