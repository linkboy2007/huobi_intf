#-*- coding:utf-8 -*-
import hashlib
import datetime 
import time
import os
import pandas as pd
import json
import requests
from requests.adapters import HTTPAdapter

MP_KEY = 'e10adc3949ba59abbe56e057f20f883e' #数字签名校验码

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
def request_http_intf(request_addr, request_url, requestBody, soft_type='pc'):
    time_stamp = str(round(time.mktime(datetime.datetime.now().timetuple())))
    sig = create_sig(request_url, soft_type, time_stamp)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    s.keep_alive = False # 关闭多余连接
    header = {}
    header["Content-Type"] = 'application/json; charset=utf-8'
    header["MP-TIMESTAMP"] = time_stamp  
    header["MP-FRONT-TYPE"] = soft_type 
    header["MP-SIG"] = sig
    rsp = s.post(request_addr + request_url, data=json.dumps(requestBody), headers=header)     
    ret_json = json.loads(rsp.text)
    if rsp.status_code == 200:
        if not 'errmsg' in ret_json.keys():
            return True, ret_json['return_result']
        else:
            return False, ret_json["errmsg"]
    else:
        return False, rsp.text

def Calc_Run_Time(func):            #计算用时的函数装饰器
    def wrapper(*args,**kwargs): 
        local_time = time.time();          res=func(*args, **kwargs)
        print('[%s] 函数运行时间：%.3f 秒' % (func.__name__ ,time.time() - local_time)); return res 
    return wrapper

@Calc_Run_Time
def get_new_price(test_dt):
    request_addr = 'http://127.0.0.1:8005'
    request_url = '/get_price'  #写入策略信息
    #日数据
    requestBody = {
        "security": "btc.usdt",
        "end_date": test_dt,
        "frequency": "1m",
        "count":1,
        "fields":[
            "close"
        ]
    }
    ret, res = request_http_intf(request_addr, request_url, requestBody)
    if ret:    
        df = pd.DataFrame.from_dict(res, orient='index')   
        df.index = pd.to_datetime(df.index, unit='ms')    
        print(df)
    else:
        print(res)

@Calc_Run_Time
def get_info(test_dt):
    request_addr = 'http://127.0.0.1:8005'
    request_url = '/info'  #写入策略信息
    #日数据
    requestBody = {}
    ret, res = request_http_intf(request_addr, request_url, requestBody)
    if ret:    
        df = pd.DataFrame.from_dict(res, orient='index')   
        #df.index = pd.to_datetime(df.index, unit='ms')    
        print(df)
    else:
        print(res)

# 程序入口函数
if __name__ == "__main__":
    test_dt = '2021-04-25 09:00:01'
    get_new_price(test_dt)
    get_info(test_dt)

    