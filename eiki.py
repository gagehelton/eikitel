from telnetlib import Telnet
from helpers import required_args
from logg3r import Log
import json

_LOG_PATH = "./test_logs/"
_INIT_LOGGER = Log(log_path=_LOG_PATH,name='init'.format(**self.__dict__),level=1)
_PORT = 3023
_TIMEOUT = 5
_COMMANDS = json.load(open("./commands.json","r"))

class Eiki():
    def __init__(self,**kwargs):
        required = {"ip":str,"name":str}
        success,error = required_args(kwargs,required)
        if(success):
            self.__dict__.update(**kwargs)
            self.logger = Log(log_path=_LOG_PATH,
                                name=self.name+"_"+self.ip.replace(".","-"),
                                level=1)
            self.session = False
            self.state = -1 #-1 = un-set value or other error
            self.control(3)
        else:
            _INIT_LOGGER.log(lineno()+"ERROR: {}".format(error),5)            

    def control(self,**kwargs):
        required = {"command":str}
        success,error = required_args(kwargs,required)
        if(success):
            if(kwargs['command'] in _COMMANDS):
            self.session = Telnet(self.ip,port=_PORT,timeout=_TIMEOUT)
            if(self.session):
                self.session.write(b'{}\n\r'.format(_COMMANDS['command']))
                #READ HERE AND SET PROJECTOR STATE 
                #SEND REQUEST FOR VALUE HERE... IDK
                self.session.close()
                return True #ACTUAL PROJECTOR STATE 0=off 1=on -1=error
            else:
                self.logger.log(lineno()+"Connection Failed! {}".format(self.session),5)
                return -1
        else:
            self.logger.log(lineno()+"ERROR: {}".format(error),5)
            return -1

if __name__ == "__main__":
    x = projector(ip="192.168.1.2",name="front")
    print(x.__dict__)