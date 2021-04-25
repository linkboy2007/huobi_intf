#-*- coding:utf-8 -*-
import hashlib
import datetime 
import time
import os
import json
import requests
from public.const import *

#根据输入字符串生成一个md5串
def getmd5(str):
    m1 = hashlib.md5()
    m1.update(str.encode("utf-8"))
    md5str = m1.hexdigest()
    return md5str

def create_sig(url_in, front_type_in, time_stamp_in):
    str = 'url=%s&front_type=%s&time_stamp=%s&key=%s' % (url_in, front_type_in, time_stamp_in, MP_KEY)
    chenk_md5 = getmd5(str)
    return chenk_md5

#调用http接口
#request_addr 接口地址，如http://168.0.0.80:8001
#request_url url地址，如 /login/add
#MP_KEY 秘钥
#requestBody 请求的json数据 
#db_name 连接的数据库名称
#soft_type 软件类型pc或app
def request_http_intf(request_addr, request_url, requestBody, db_name, soft_type):
    time_stamp = str(round(time.mktime(datetime.datetime.now().timetuple())))
    sig = create_sig(request_url, soft_type, time_stamp)
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    header = {}
    header["Content-Type"] = 'application/json; charset=utf-8'
    header["MP-TIMESTAMP"] = time_stamp  
    header["MP-FRONT-TYPE"] = soft_type 
    header["MP-SIG"] = sig
    header["MP-SPEC-ID"] = db_name    
    rsp = requests.post(request_addr + request_url, data=json.dumps(requestBody), headers=header)     
    ret_json = json.loads(rsp.text)
    if rsp.status_code == 200:
        if ret_json["code"] == 0:
            return True, '', ret_json['result']
        else:
            return False, ret_json["msg"], ''
    else:
        return False, rsp.text, ''