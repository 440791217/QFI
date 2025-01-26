import json
import os
import threading
import time


class Monitor(threading.Thread):

    def __init__(self):
        super().__init__()
        self.result_dir_path = None
        pass

    def set_result_dir_path(self, result_dir_path):
        self.result_dir_path = result_dir_path

    def check_uni(self, ln):
        flag = ''
        if 'i:' in ln or 'j:' in ln or 'result:' in ln:
            flag = 'sdc'
        return flag

    def parse_lines(self, fpath):
        start_main = 0
        start_intermain = 0
        INJ_HEAD = 0
        INJ_END = 0
        FAULT_DETECTED_RWC = 0
        FAULT_DETECTED_DWC =0
        HardFault_Handler =0
        flag = 'masked'
        flag1 = 'none'
        info=''
        bn=0
        with open(fpath, 'r') as rf:
            lines = []
            for ln in rf.readlines():
                ln = ln.strip()
                if 'INJ_HEAD>>' in ln and '<<INJ_END':
                    info=ln.replace('INJ_HEAD>>','').replace('<<INJ_END','')
                    info=json.loads(info)
                if 'INJ_HEAD' in ln:
                    INJ_HEAD += 1
                if 'INJ_END' in ln:
                    INJ_END += 1
                if 'start main' in ln:
                    start_main += 1
                if INJ_END==0:
                    continue
                if 'FAULT_DETECTED_DWC' in ln:
                    FAULT_DETECTED_DWC += 1
                if 'FAULT_DETECTED_RWC' in ln:
                    FAULT_DETECTED_RWC+=1
                if 'HardFault_Handler' in ln:
                    HardFault_Handler+=1
                if INJ_END > 0 and len(ln) > 0:
                    lines.append(ln)
            if FAULT_DETECTED_DWC > 0:
                flag1 = 'dwc'
            elif FAULT_DETECTED_RWC > 0:
                flag1 = 'rwc'

            for ln in lines:
                f = self.check_uni(ln)
                # f=self.check_crc(ln)
                if f == 'sdc':
                    # print('sdc==>ln:{}-----fpath:{}',ln,fpath)
                    flag = f
                if ">>b'\\n'" in ln:
                    bn+=1
            if bn==0:
                flag='due'
                # print('due fpath',fpath)
            elif start_main > 1:
                flag = 'due'
                # print('due fpath',fpath)
            # else:
            #     for ln in lines:
            #         f = self.check_uni(ln)
            #         # f=self.check_crc(ln)
            #         if f == 'sdc':
            #             # print('sdc==>ln:{}-----fpath:{}',ln,fpath)
            #             flag = f

        return flag,flag1,info

    def run(self):
        assert self.result_dir_path
        done_file = []
        result_map = {
            'sdc': 0,
            'due': 0,
            'masked': 0,
            'total': 0,
        }
        result_map1 = {
            'none':0,
            'dwc': 0,
            'rwc': 0,
            'total':0,
        }
        result_map2={
            
        }
        while True:
            dirs = sorted(os.listdir(self.result_dir_path))
            for i in range(len(dirs)-1):
                f=dirs[i]
                # print(f)
                if f not in done_file:
                    fpath = os.path.join(self.result_dir_path, f)
                    flag,flag1,info = self.parse_lines(fpath=fpath)
                    done_file.append(f)
                    if info =='':
                        continue
                    result_map[flag] += 1
                    result_map['total'] += 1
                    result_map1[flag1] += 1
                    result_map1['total'] += 1
                    regs=info['regs']
                    reg_name=regs[0]['name']
                    if reg_name not in result_map2.keys():
                        result_map2[reg_name]={
                            'sdc':0,
                            'due':0,
                            'masked':0,
                            'total':0,
                        }
                    result_map2[reg_name][flag]+=1
                    result_map2[reg_name]['total']+=1
            time.sleep(2)
            print('result_map',result_map)
            print('result_map1', result_map1)
            for reg in sorted(result_map2.keys()):
                print('reg {},{},{},{}'.format(reg,result_map2[reg]['sdc'],result_map2[reg]['due'],
                                               result_map2[reg]['masked']))

if __name__ == '__main__':
    monitor = Monitor()
    # monitor.set_result_dir_path(result_dir_path='/home/mark/data/PycharmProjects/QFI/app/stm32F407_mk/result/RF/1')
    monitor.set_result_dir_path(result_dir_path='/home/mark/data/PycharmProjects/QFI/results/max_rwc/stm32F407_mk/result/RF/1')
    # monitor.set_result_dir_path(result_dir_path='/home/mark/data/PycharmProjects/QFI/results/mm_dwc/stm32F407_mk/result/RF/1')
    # monitor.set_result_dir_path(result_dir_path='/home/mark/data/PycharmProjects/QFI/results/mm_tmr/stm32F407_mk/result/RF/1')
    monitor.start()
    #
