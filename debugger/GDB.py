import time
from pygdbmi.gdbcontroller import GdbController
import threading
from system.Logger import Logger

def debug(msg):
    Logger.debug(msg)
#gdb=arm-none-eabi-gdb

class GDB(threading.Thread):

    def __init__(self,elf_bin=None,gdb_bin=None,port=None,before_tm=None,after_tm=1):
        super().__init__()
        assert (elf_bin)
        assert (gdb_bin)
        assert (before_tm)
        assert (port)
        command = [gdb_bin, "--nx", "--quiet",
                   "--interpreter=mi3", elf_bin]
        self.command=command
        # self.exec_file=exec_file
        self.gdbmi=None
        self.port=port
        self.before_tm=before_tm
        self.after_tm=after_tm
        pass

    def send(self,command=None):
        assert (command)
        response=self.gdbmi.write(command)
        debug(response)

    def launch(self):
        self.gdbmi = GdbController(self.command)
        debug(self.gdbmi.command)  # print actual command run as subprocess

    def extended_remote(self):
        self.send(command='target extended-remote:{}'.format(self.port))

    def init(self):
        commands=[
            'set confirm off',
            'set pagination off',
            'set history save',
            'set verbose off',
            'set print pretty on',
            'set print arrary off',
            'set print arrary-indexes on',
            'set python print-stack full'
        ]
        for command in commands:
            self.send(command=command)



    def begin(self):
        self.send(command='run &')

    def nexti(self):
        self.send(command='nexti')

    def go_ahead(self):
        self.send(command='continue &')

    def halt(self):
        self.send(command='interrupt')

    def get_register(self,reg=None):
        assert (reg)
        self.send(command='print ${}'.format(reg))

    def set_register(self,reg=None):
        assert (reg)
        self.send(command='set ${} = {}'.format(reg,0))

    def quit(self):
        response = self.gdbmi.exit()
        debug(response)

    def test(self):
        response = self.gdbmi.write('11 {}'.format(self.exec_file))
        debug(response)

    def run(self):
        self.launch()
        self.init()
        self.extended_remote()
        self.begin()
        self.halt()
        for i in range(100):
            self.nexti()
        # self.go_ahead()
        # time.sleep(self.before_tm)
        # self.halt()
        # self.get_register(reg='r1')
        # self.get_register(reg='r2')
        # self.set_register(reg='r1')
        # self.get_register(reg='r1')
        # self.go_ahead()
        # time.sleep(self.after_tm)
        self.quit()
        # self.test()

        pass


if __name__ == '__main__':
    gdb=GDB(elf_bin='/home/mark/data/PycharmProjects/QFI/app/stm32f407_test/stm32f407_test.elf',
            gdb_bin='arm-none-eabi-gdb',
            port=2331,
            before_tm=1
            )
    gdb.start()
