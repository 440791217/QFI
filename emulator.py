import subprocess
from logger import Logger
from constant import Constant
from appSys import AppSys


class Emulator:

    def __init__(self, **args):
        Logger.debug("Emulator Init")
        pass

    def trace_inst(self):
        fp = Constant.get_file_path_app_trace_inst()
        qemu_args = Constant.get_qemu_trace_inst_args()
        ###################trace inst log
        wf = open(fp, 'w')
        rf = open(fp, 'r')
        proc = subprocess.Popen(qemu_args, text=True, stdout=wf)
        while True:
            AppSys.sleep(2)
            current = len(rf.readlines())
            Logger.debug('current:{}'.format(current))
            if current == 0:
                break
        if proc.poll() is None:
            proc.terminate()
        wf.close()
        rf.close()
        ##################wash log
        fp1 = Constant.get_file_path_app_trace_inst_wash()
        wf = open(fp1, 'w')
        rf = open(fp, 'r')
        ls = rf.readlines()
        for l in ls:
            if 'my_qemu_addr' in l:
                wf.write(l)
        wf.close()
        rf.close()

    def main(self):
        self.trace_inst()
        pass


if __name__ == '__main__':
    emulator = Emulator()
    emulator.main()
