import json
import time
import os
import shutil


class Utils:
    def __init__(self, logger=None):
        self.logger = logger
        self.logger.debug('init successfully!')
        pass

    @staticmethod
    def sleep(self, tm=1):
        time.sleep(tm)
        self.logger.debug('sleep in {} sec!'.format(tm))

    def delete_by_path(self,fp):
        if os.path.exists(fp):
            shutil.rmtree(fp)
            self.logger.debug('delete path:{}'.format(fp))
        else:
            self.logger.debug('path does not exist:{}'.format(fp))

    def except_with_msg(self,code=-1, msg=None):
        if msg is not None:
            self.logger.error(msg)
        exit(code)

    def except_if_not_exists(self,fp,msg=None):
        if os.path.exists(fp) is False:
            if msg is not None:
                self.logger.error(msg)
                self.logger.error(msg)
            exit(-1)

    ###########################################json
    def dump_by_json(self, fp, data):
        with open(fp, 'w') as wf:
            json.dump(data, wf, indent=2)
            self.logger.debug('dump_by_json:{}!'.format(fp))

    def load_by_json(self, fp):
        with open(fp, 'r') as rf:
            data = json.load(rf)
            self.logger.debug('load_by_json:{}!'.format(fp))
        return data
