#-*- coding:utf-8 -*-
import hashlib
import datetime 
import time
import pandas as pd
import json
import requests
#这两个参数的默认设置都是False
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

MP_KEY = 'e10adc3949ba59abbe56e057f20f883e' #数字签名校验码

#得到yyyy-mm-dd hh:ss:nn格式的字符串
def fmt_now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def Calc_Run_Time(func):            #计算用时的函数装饰器
    def wrapper(*args,**kwargs): 
        local_time = time.time();          res=func(*args, **kwargs)
        print('[%s] 函数运行时间：%.3f 秒' % (func.__name__ ,time.time() - local_time)); return res 
    return wrapper

@Calc_Run_Time
def get_info():
    request_addr = 'http://127.0.0.1:8005'
    #日数据
    df=pd.DataFrame()
    time_stamp = str(round(time.mktime(datetime.datetime.now().timetuple())))
    sig = create_sig('/info', "pc", time_stamp)
    header = {}
    header["Content-Type"] = 'application/json; charset=utf-8' 
    header["MP-SIG"] = sig    
    header["MP-TIMESTAMP"] = time_stamp   
    header["MP-FRONT-TYPE"] = "pc"    
    res = requests.post(url=request_addr + "/info", json={}, headers=header) 
    rstr = json.loads(res._content) 
    if 'return_result' in rstr.keys():       
        df = pd.DataFrame.from_dict(rstr['return_result'], orient='index')
        if len(df) == 0: 
            return df      #df为空直接返回
        return df
    else:
        print(rstr)  

def get_price(security, start_date=None, end_date=None, frequency='1d', fields=None, count=None, fq='pre'):
    request_addr = 'http://127.0.0.1:8005'
    time_stamp = str(round(time.mktime(datetime.datetime.now().timetuple())))
    df=pd.DataFrame()
    sig = create_sig('/get_price', "pc", time_stamp)
    header = {}
    header["Content-Type"] = 'application/json; charset=utf-8' 
    header["MP-SIG"] = sig    
    header["MP-TIMESTAMP"] = time_stamp   
    header["MP-FRONT-TYPE"] = "pc"            
    
    start_date=fmt_now_time() if start_date else None       
    end_date=fmt_now_time() if end_date else None   
    post_data = {'security':security, 'start_date': start_date, 'end_date': end_date, 'count': count, 'frequency': frequency,'fields':fields,'fq':fq }    

    try: 
        res = requests.post(url=request_addr + "/get_price", json=post_data, headers=header)  
    except: 
        return df
    rstr = json.loads(res._content) 
    if 'return_result' in rstr.keys():       
        df = pd.DataFrame.from_dict(rstr['return_result'], orient='index')
        if len(df)==0: 
            return df      #df为空直接返回
        df.index=pd.to_datetime(df.index, unit='ms');    
        return df    

# 程序入口函数
if __name__ == "__main__":
    #1分钟的数据获取
    df = get_price('btc.usdt', end_date=fmt_now_time(), count=10, frequency='1m', fields=['open','close', 'low', 'high'])
    print(df)
    #日线的数据获取
    df = get_price('btc.usdt', end_date=fmt_now_time(), count=10, frequency='1d', fields=['open','close', 'low', 'high'])
    print(df)
    #4小时的数据获取
    df = get_price('btc.usdt', end_date=fmt_now_time(), count=10, frequency='4h', fields=['open','close', 'low', 'high'])
    print(df)
    #1小时的数据获取
    df = get_price('btc.usdt', end_date=fmt_now_time(), count=10, frequency='60m', fields=['open','close', 'low', 'high'])
    print(df)
    #取到btc和eth的实时分钟线数据
    df = get_info()
    print(df)