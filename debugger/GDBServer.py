import subprocess
import threading
import time

from system.Config import Config
from system.Logger import Logger


class JLinkGDBServer(threading.Thread):

    def __init__(self, log_file=None):
        super().__init__()
        assert log_file
        self.log_file = log_file
        self.command = None
        self.proc = None
        self.th = None
        self.running = False

    def connect(self, ff):
        self.command = 'JLinkGDBServer -device STM32F407ZG -if swd -nogui'.split()
        Logger.debug('connect command:{}'.format(self.command))
        self.proc = subprocess.Popen(self.command, stdout=ff, stderr=ff,
                                     text=True)
        self.running = True

    def poll(self, ff):
        while True:
            time.sleep(1)
            outs = ff.readlines()
            for i in range(len(outs)):
                out = outs[i]
                out = out.strip()
                if "ERROR" in out:
                    Logger.error('JLink GDBServer stdout1:{}'.format(out))
                    self.close()
                    break
                else:
                    Logger.debug('JLink GDBServer stdout2:{}'.format(out))
            if not self.running:
                self.close()
                Logger.error('JLink GDBServer active closed.')
                break
            elif self.proc.poll():
                Logger.error('JLink GDBServer passive closed.')
                self.close()
                break



    def close(self):
        self.running = False
        if not self.proc.poll():
            self.proc.terminate()
            self.proc.terminate()
        Logger.error('Close JLink GDBServer.')


    def run(self):
        with open(self.log_file, 'w') as wf:
            with open(self.log_file,'r') as rf:
                self.connect(ff=wf)
                self.poll(ff=rf)
                # time.sleep(1)
                outs = rf.readlines()
                for i in range(len(outs)):
                    out = outs[i]
                    out = out.strip()
                    Logger.error(out)


if __name__ == '__main__':
    GDBServer = JLinkGDBServer(log_file=Config.get_file_path_app_gdb_server_log())
    GDBServer.start()
