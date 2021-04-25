#-*- coding:utf-8 -*-
import tornado.web
import datetime
import time
from tornado.options import define, options

from public.pubfunc import *
from public.const import *
from dbc import *
import sys
import platform

#/usr/local/lib/python3.6/dist-packages 默认安装路径
class BaseHandle(tornado.web.RequestHandler):
    """基类"""
    
    #----------------------------------------------------------------------
    #@tornado.web.authenticated
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")     #跨域
        self.set_header("Access-Control-Allow-Headers", "MP-TIMESTAMP,MP-ACCESS-TOKEN, \
                         MP-FRONT-TYPE,MP-SIG,Content-Type,X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
        self.set_header('Server', 'spec server')
        
    #定义一个响应OPTIONS 请求，不用作任务处理
    def options(self):
        pass
    
    #404页面
    def get(self):
        self.write_error(404)
    
    #TypeError: Object of type 'datetime' is not JSON serializable
    #这样的错误是数据引起的
    def write_error(self, status_code, **kwargs):
        print('write_error:', status_code, kwargs)
        self.write({'error:':'write_error: ' + str(status_code)})           
    
    #验证token和时间戳
    def prepare(self):
        print('prepare:', self.request.uri, self.request.body)
        system = platform.system()    
        debug_mode = use_debug_mode(sys.argv)
        if not debug_mode:
            try:
                self.debug_mode = False
                self.remote_ip = self.request.remote_ip  
                time_stamp = self.request.headers.get(MP_TIMESTAMP)
                front_type = self.request.headers.get(MP_FRONT_TYPE)
                if (time_stamp == None) or (time_stamp == '') or \
                        (front_type == None) or (front_type == ''):
                    if time_stamp == None or time_stamp == '':
                        self.finish(err_json('时间戳为空，请发送时间戳后重新再试', API_INTERNAL_ERROR)) 
                    elif front_type == None or front_type == '':
                        self.finish(err_json('软件类型为空，请发送后再试', API_INTERNAL_ERROR)) 
                else:
                    clent_time_stamp = int(time_stamp)
                    svr_time_stamp = time.mktime(datetime.datetime.now().timetuple())
                    if abs(svr_time_stamp - clent_time_stamp) > TIME_DIFF:
                        self.finish(err_json('与服务器时间相差超过5分钟，请调整时间后重新再试', API_TIME_ERROR))  
                    else:
                        self.url = self.request.uri                                                       
                        sig_str = self.request.headers.get(MP_SIG)
                        if sig_str != None:
                            is_check = check_sig(self.request.uri, front_type, time_stamp, sig_str)
                            if not is_check:
                                self.finish(err_json('数字签名不正确', API_NO_PERMISSION))
                        else:
                            self.finish(err_json('请提交数字签名', API_NO_PERMISSION))                             
            except Exception as e:
                print('prepare error = ', repr(e), ' uri=', self.request.uri, ' body=' + self.request.body)
                self.finish(err_json('prepare访问错误:' + repr(e), API_INTERNAL_ERROR))
        elif debug_mode and system == 'Windows':
            self.debug_mode = True
            self.url = self.request.uri
            self.remote_ip = self.request.remote_ip