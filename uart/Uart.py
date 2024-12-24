import datetime
import time
import serial
import serial.tools.list_ports
import glob
import threading

from system.Logger import Logger


class Uart(threading.Thread):

    def __init__(self):
        super().__init__()
        self.running=False
        self.com=serial.Serial()
        self.com.port = None  # 设置端口号
        self.com.baudrate = 115200  # 设置波特率
        self.com.bytesize = 8  # 设置数据位
        self.com.stopbits = 1  # 设置停止位
        self.callback=None
        pass

    def config(self,port=None,baudrate=115200,bytesize=8,stopbits=1):
        assert (port)
        self.com.port=port
        self.com.baudrate=baudrate
        self.com.bytesize=bytesize
        self.com.stopbits=stopbits
        self.com.timeout=0.1

    def set_callback(self,callback=None):
        self.callback=callback


    def open(self):
        self.com.open()
        self.running=self.com.is_open


    def close(self):
        self.running=False
        self.callback=None
        time.sleep(0.3)
        self.com.close()

    def read(self):
        # data = self.com.read(size=self.com.in_waiting)

        data = self.com.readline()
        if self.callback is None or len(data)==0:
            pass
        else:
            self.callback(data)


    def run(self):
        while self.running:
            # if self.com.in_waiting>0:
            self.read()

            # now = datetime.datetime.now()
            # tf = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            # tf_data = '{}>>{}\n\r'.format(tf, data)
            # self.wf.write(tf_data)

if __name__=='__main__':
    devices = glob.glob('/dev/ttyCH*')
    for i in range(5):
        with open('/home/mark/data/PycharmProjects/QFI/app/stm32f407_test/tmp/test{}.txt'.format(i), 'w') as wf:
            uart = Uart()
            uart.config(port=devices[0])
            def callback(data):
                now = datetime.datetime.now()
                tf = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                tf_data = '{}AABBCCDD>>{}'.format(tf, data)
                wf.write(tf_data)
            uart.set_callback(callback=callback)
            uart.open()
            print(devices)
            print('i:',i)
            assert (uart.com.is_open)
            uart.start()
            time.sleep(2)
            uart.close()
#
#     # for p in plist:
#     #     print('plist:', p)