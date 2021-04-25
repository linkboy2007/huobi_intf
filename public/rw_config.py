# coding:utf8
import configparser
import os

#proDir = os.path.split(os.path.realpath(__file__))[0]
#configPath = os.path.join(proDir, "config.ini")
configpath = "./config/sysconfig.ini"
#将整个读取ini的过程封装成一个类

class rwcfg:
    def __init__(self):
        self.cf = configparser.ConfigParser()#调用读取配置模块中的类
        self.cf.read(configpath)#读取文件
    def read(self, par, name, value):        
        if (self.cf.has_section(par)) and  (self.cf.has_option(par, name)):
            value = self.cf.get(par, name)#通过get方法，读取需要的参数
        return value
    def write(self, par, name, value):      
        if not self.cf.has_section(par):
            self.cf.add_section(par)        
        self.cf.set(par, name, value)
        with open(configpath,"w+") as f:
            self.cf.write(f)
        return value 


