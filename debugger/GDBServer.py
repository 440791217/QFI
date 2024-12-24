import subprocess
import threading
import time

from system.Logger import Logger

JLINK_RET_CODE_MAP = {
    0: 'No error. GDB Server closed normally.',
    -1: 'Unknown error. Should not happen.',
    -2: 'Failed to open listener port (Default: 2331).',
    -3: 'Could not connect to target. No target voltage detected or connection failed.',
    -4: 'Failed to accept a connection from GDB.',
    -5: 'Failed to parse the command line options, wrong or missing command line parameter.',
    -6: 'Unknown or no device name set.',
    -7: 'Failed to connect to J-Link.'
}


class GDBServer(threading.Thread):
    def __init__(self):
        super().__init__()
        # assert log_file
        self.log_file = None
        self.command = None
        self.proc = None
        self.th = None
        self.running = False
        self.returncode = 0
        self.returnmsg = ''

    def set_log_file(self, log_file):
        self.log_file = log_file

    def set_command(self, command):
        self.command = command

    def close(self):
        assert (self.proc)
        self.proc.terminate()
        self.running = False

    def run(self):
        assert self.command
        self.running = True
        self.proc = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True)
        std, err = self.proc.communicate()
        # while self.proc.poll() is None:
        #     time.sleep(0.5)
        self.returncode = self.proc.poll()
        if self.returncode > 127:
            self.returncode = self.returncode - 256
        self.running = False
        ret_code_map = JLINK_RET_CODE_MAP
        if self.returncode in ret_code_map.keys():
            ret_msg = ret_code_map[self.returncode]
        else:
            ret_msg = 'Unkown Error Message!'
        self.returnmsg=ret_msg
        Logger.error('ret code:{}'.format(self.returncode))
        Logger.error('ret message:{}'.format(ret_msg))
        pass


if __name__ == '__main__':
    gdbServer = GDBServer()
    gdbServer.set_command(
        command='JLinkGDBServer -port 2331 -device STM32F407ZG -endian little -speed 4000 -if swd -vd -nogui'.split())
    gdbServer.start()

