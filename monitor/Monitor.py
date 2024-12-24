import os
import threading
import time
import re

class Monitor(threading.Thread):

    def __init__(self):
        super().__init__()
        self.result_dir_path = None
        pass

    def set_result_dir_path(self, result_dir_path):
        self.result_dir_path = result_dir_path

    def parse_lines(self, fpath):
        start_main = 0
        start_intermain = 0
        INJ_HEAD = 0
        INJ_END = 0
        flag = 'masked'
        with open(fpath, 'r') as rf:
            lines = []
            for ln in rf.readlines():
                ln = ln.strip()
                if 'start main' in ln:
                    start_main += 1
                if 'INJ_HEAD' in ln:
                    INJ_HEAD += 1
                if 'INJ_END' in ln:
                    INJ_END += 1
                if INJ_END > 0 and len(ln) > 0:
                    lines.append(ln)
            if start_main>1:
                flag='due'
            else:
                for ln in lines:
                    # l=ln[ln.find("'")+1:ln.rfind("'")]
                    if "'result:" in ln and "\\n'" in ln:
                        l=ln[ln.find('result:'):ln.find('\\n')]
                        # print(l)
                        if 'result: 8874.' not in l:
                            print(l,fpath)
                            flag='sdc'
        return flag

    def run(self):
        assert self.result_dir_path
        while True:
            result_map={
                'sdc':0,
                'due':0,
                'masked':0,
            }
            dirs = sorted(os.listdir(self.result_dir_path))
            for f in dirs:
                # print(f)
                fpath = os.path.join(self.result_dir_path, f)
                flag=self.parse_lines(fpath=fpath)
                result_map[flag]+=1
            time.sleep(2)
            print(result_map)


if __name__ == '__main__':
    monitor = Monitor()
    monitor.set_result_dir_path(result_dir_path='/home/mark/data/PycharmProjects/QFI/app/stm32F407_mk/result/RF/1')
    monitor.start()
    #
