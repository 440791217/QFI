import subprocess
import yaml




def disassemble(**args):
    config=args['config']
    binPath=config['binPath']
    binObjDump=config['binObjDump']
    result = subprocess.run([binObjDump, binPath,'-S'], text=True)
    if result.returncode!=0:
        print("errors occur in disassemble!\n")
        exit(-1)

    pass


if __name__=='__main__':
    with open("app/stm32f100_mk/config/config.yaml","r") as rf:
        config=yaml.safe_load(rf)
    print(config)
    disassemble(config=config)
    #disassemble(pathBin=PATH_BIN)