import glob
import json
import threading
import time
import datetime

from pygdbmi.gdbcontroller import GdbController
from soupsieve.util import lower

from system.Constant import Constant
from system.Logger import Logger
from uart.Uart import Uart

WF_HEAD='WF_HEAD'
WF_END='WF_END'
INJ_HEAD='INJ_HEAD'
INJ_END='INJ_END'

class GDB(threading.Thread):

    SUPPORT_MODES=[Constant.FAULT_MODE_RF]

    @staticmethod
    def debug(msg):
        Logger.debug(msg)

    @staticmethod
    def bit_flip(value, flip_pos):
        value ^= (1 << flip_pos)
        return value


    def __init__(self):
        super().__init__()
        self.elf_bin = None
        self.gdb_bin = None
        self.gdbmi = None
        self.port = 2331
        self.mode = Constant.FAULT_MODE_RF
        self.fault = None

    def check_init(self):
        assert self.elf_bin
        assert self.gdb_bin
        assert self.fault
        assert self.port
        assert self.mode in GDB.SUPPORT_MODES

    def set_elf_bin(self, elf_bin):
        self.elf_bin = elf_bin

    def set_gdb_bin(self, gdb_bin):
        self.gdb_bin = gdb_bin

    def set_fault(self, fault):
        self.fault = fault

    def get_fault(self):
        return self.fault

    def set_mode(self, mode):
        self.mode = mode

    def set_port(self, port):
        self.port = port

    def send(self, command=None):
        assert (command)
        response = self.gdbmi.write(command)
        GDB.debug(response)
        return response

    def launch(self):
        command = [self.gdb_bin, "--nx", "--quiet",
                   "--interpreter=mi3", self.elf_bin]
        self.gdbmi = GdbController(command)
        GDB.debug(self.gdbmi.command)  # print actual command run as subprocess

    def remote(self):
        status=False
        response=self.send(command='target remote:{}'.format(self.port))
        for res in response:
            if res['type'] == 'console':
                if 'Remote debugging using :{}'.format(self.port) in res['payload']:
                    status=True
        return status


    def extended_remote(self):
        self.send(command='target extended-remote:{}'.format(self.port))

    def init(self):
        commands = [
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
        self.send(command='monitor reset')

    def nexti(self):
        self.send(command='nexti')

    def stepi(self):
        self.send(command='stepi')
        self.send(command='display $pc')

    def go_ahead(self):
        self.send(command='monitor go')

    def halt(self):
        self.send(command='monitor halt')

    def get_register(self, name=None):
        assert (name)
        rsp=self.send(command='monitor reg {}'.format(name))
        value=None
        for ln in rsp:
            if ln['type']=='target':
                payload=ln['payload']
                name1=payload[payload.find('(')+1:payload.find(')')].split('=')[0].strip()
                value=payload[payload.find('(')+1:payload.find(')')].split('=')[1].strip()
                assert (lower(name)==lower(name1))
        GDB.debug('registers name:{},value:{}'.format(name,value))
        return value

    def set_register(self, name=None,value=None):
        assert (name)
        assert value
        self.send(command='monitor reg {} = {}'.format(name, value))

    def quit(self):
        response = self.gdbmi.exit()
        GDB.debug(response)

    def test(self):
        response = self.gdbmi.write('11 {}'.format(self.exec_file))
        GDB.debug(response)

    def profile_inst(self):
        # self.launch()
        # self.init()
        # self.extended_remote()
        # self.begin()
        # self.halt()
        # self.stepi()
        pass

    # def

    def do_inject_rf(self):
        regs=self.fault['regs']
        GDB.debug(self.fault)
        # step.1:get registers
        for reg in regs:
            name = reg['name']
            flips = reg['flips']
            before_value = self.get_register(name=name)
            after_value = int(before_value, 16)
            for pos in flips:
                after_value = GDB.bit_flip(value=after_value, flip_pos=pos)
            after_value = hex(after_value)
            self.set_register(name=name, value=after_value)
            after_value1 = self.get_register(name=name)
            assert (int(after_value, 16) == int(after_value1, 16))
            reg['before_value'] = before_value
            reg['after_value'] = after_value
        Logger.debug(self.fault)
        pass

    def run(self):
        log_file_path=self.fault['log_file_path']
        devices = glob.glob('/dev/ttyCH*')
        with open(log_file_path,'w') as wf:
            uart = Uart()
            uart.config(port=devices[0])
            def callback(data):
                now = datetime.datetime.now()
                tf = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                tf_data = '{}>>{}\n\r'.format(tf, data)
                wf.write(tf_data)
            uart.set_callback(callback=callback)
            uart.open()
            assert (uart.com.is_open)
            uart.start()
            wf.write('{}\n'.format(WF_HEAD))
            self.check_init()
            before_tm=self.fault['before_tm']
            after_tm=1
            #step1:launch
            self.launch()
            self.init()
            status=self.remote()
            assert 'Remote connection is lost.' and status
            self.begin()
            self.go_ahead()
            #step2:wait for random seconds
            time.sleep(before_tm)
            self.halt()
            #step3:inject faults
            if self.mode==Constant.FAULT_MODE_RF:
                self.do_inject_rf()
            inj_info='{}>>{}<<{}\n'.format(INJ_HEAD,json.dumps(self.fault),INJ_END)
            wf.write(inj_info)
            #step4:resume execution
            self.go_ahead()
            time.sleep(after_tm)
            uart.close()
            self.halt()
            self.quit()
            wf.write('{}\n'.format(WF_END))
        pass


if __name__ == '__main__':
    gdb = GDB()
    gdb.set_elf_bin('/home/mark/data/PycharmProjects/QFI/app/stm32f407_test/stm32f407_test.elf')
    gdb.set_gdb_bin('arm-none-eabi-gdb')
    gdb.set_fault(  {
    "id": 1,
    "regs": [
      {
        "name": "r6",
        "flips": [
          16
        ],
        "before_value": -1,
        "after_value": -1
      }
    ],
    "before_tm": 0.6816946318017266,
    "injected": True
  })
    gdb.start()
    gdb.join()
