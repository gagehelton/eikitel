from telnetlib import Telnet
from helpers import required_args,lineno
from logg3r import Log
import json

config = json.load(open("./config.json","r"))

_INIT_LOGGER = Log(log_path=config['log_path'],name='eiki_init',level=1)

class Eiki():
    def __init__(self,**kwargs):
        required = {"ip":str,"name":str}
        success,error = required_args(kwargs,required)
        if(success):
            self.__dict__.update(**kwargs)
            self.logger = Log(log_path=config['log_path'],
                                name=self.name+"_"+self.ip.replace(".","-").replace(" ","_").lower(),
                                level=1)
            self.session = False
            self.state = 1
            #self.control(command="status")
        else:
            _INIT_LOGGER.log(lineno()+"ERROR: {}".format(error),5)            

    def control(self,**kwargs):
        required = {"command":str}
        success,error = required_args(kwargs,required)
        if(success):
            if(kwargs['command'] in config['commands']):
                self.session = Telnet(self.ip,port=config['port'],timeout=config['timeout'])
                if(self.session):
                    self.session.write('{}\n\r'.format(config['commands'][kwargs['command']]).encode('utf-8'))
                    self.logger.log(lineno()+"Session: Command {} | {}".format(kwargs['command'],self.session.read_very_eager(),1))
                    self.session.close()
                    self.state = 1 #ACTUAL PROJECTOR STATE 0=off 1=on -1=error
                    return True
                else:
                    self.logger.log(lineno()+"Connection Failed! {}".format(self.session),5)
                    self.state = 0
                    return False
        else:
            self.logger.log(lineno()+"ERROR: {}".format(error),5)
            return False

if __name__ == "__main__":
    x = Eiki(ip="192.168.1.2",name="front")
    print(x.__dict__)