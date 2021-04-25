#-*- coding:utf-8 -*-
import hashlib
import datetime 
import uuid
import string
import random
import json
from public.const import *


#新的GUID
def new_guid():
    return str(uuid.uuid1()).replace('-', '')

#产生n位的随机数
def random_count(count):
    seeds = string.digits
    random_str = random.sample(seeds, k=count)
    return "".join(random_str)

#得到yyyy-mm-dd hh:ss:nn格式的字符串
def fmt_now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#得到yyyymmddhhssnn格式的字符串
def fmt_now_export_time():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

#得到yyyy-mm-dd格式的字符串
def fmt_now_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

#得到mm-dd格式的字符串
def fmt_month_day_date():
    return datetime.datetime.now().strftime("%m-%d")

#根据输入字符串生成一个md5串
def getmd5(str):
    m1 = hashlib.md5()
    m1.update(str.encode("utf-8"))
    md5str = m1.hexdigest()
    return md5str
    
def err_json(err_info, state_code):
    result_json = {"code":0, "msg":"", "result":{}}
    result_json["code"] = state_code
    result_json["msg"] = err_info
    result_json["result"] = {} 
    return result_json
    
#格式化单号里的日期 现在为190807格式(年取后两位) 小写y是年取后两位 大写Y是年取四位
def datefmt(long_date):
    ret = datetime.datetime.now().strftime("%y%m%d")
    if len(long_date) == 10:
        ret = long_date[2:4] + long_date[5:7] + long_date[8:]
    return ret
    
def dic_default(dic, key, default_value):
    if key in dic:
        return dic.get(key, default_value)
    else:
        return default_value
    
def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n < 0):
        n = abs(n)
        return datetime.date.today() - datetime.timedelta(days=n)
    else:
        return datetime.date.today() + datetime.timedelta(days=n)

#计算有效期的结束时间 天/月/年
def calc_end_time(valid_type, end_unit, end_data):
    end_time = datetime.datetime.now()
    if valid_type == 0:  #开始方式(0出售即开卡，1消费即开卡)
        end_time = datetime.datetime.now()
        if end_unit == '日':
            end_time = get_day_of_day(end_data)
        elif end_unit == '月':
            end_time = get_day_of_day(end_data * 30)
        elif end_unit == '年':
            end_time = get_day_of_day(end_data * 365)
        #加结束时分秒 end_time_str = end_time.strftime("%Y-%m-%d 23:59:59") 
        #加结束时分秒 end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    return end_time

#时间变成当天最后一分钟，比如2020-04-24 变成2020-04-24 23:59:59
def date_to_end(change_date):
    now = datetime.datetime.now()
    if type(change_date) == type(now):
        date_str = change_date.strftime("%Y-%m-%d 23:59:59")
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        return change_date

def ios_to_datetime(dt_str):
    date_fmt = '%Y-%m-%dT%H:%M:%S+08:00'
    return datetime.datetime.strptime(dt_str, date_fmt)

#两个日期字符串的相差天数
def days(str1, str2):
    date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date1 - date2).days
    return num


#检测数字签名url+front_type+time_stamp+key做md5计算
def check_sig(url_in, front_type_in, time_stamp_in, sig_in):
    is_succ = False
    str = 'url=%s&front_type=%s&time_stamp=%s&key=%s' % (url_in, front_type_in, time_stamp_in, MP_KEY)
    chenk_md5 = getmd5(str)
    if chenk_md5.upper() == sig_in.upper():
        is_succ = True
    return is_succ

#使用子路由时的判断
def use_sub_url(old_url, sys_args):
    sub_url = old_url
    if sys_args != '':
        sub_url = '/' + sys_args + old_url 
    return sub_url

def use_debug_mode(sys_args):
    use = False
    if len(sys_args) > 1:
        args = sys_args
        for i in range(1, len(args)):
            arg = args[i].lstrip("-")
            name, equals, value = arg.partition("=")  
            if name == 'debug':
                use = True 
                break 
    return use

#直接截取保留的小数位数
def digit_split(num, digit):
    num_x , num_y = str(num).split('.')
    num = float(num_x + '.' + num_y[0:digit])       
    return num 
    
#将数据库字段值转成浮点数    
def str_to_float(s):
    if s is None:
        return 0
    elif s == "None":
        return 0
    else:
        return float(str(s))
            
#判断字符串是否为合法json格式
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

#有多少位显示多少位小数，没有不显示
def float_format(digital_number):
    d_str = str(float(digital_number))
    if d_str[-2:] == '.0':
        return d_str.split('.')[0]
    else:
        return d_str

def index_of_str(s1, s2):
    n1=len(s1)
    n2=len(s2)
    for i in range(n1-n2+1):
        if s1[i:i+n2]==s2:
            return i
    else:
        return -1

def secNums(startTime, endTime):
    '''计算两个时间点之间的秒数'''
    # 计算分钟数
    startTime2 = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    endTime2 = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    seconds = (endTime2 - startTime2).seconds
    # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
    total_seconds = abs((endTime2 - startTime2).total_seconds())
    # 来获取准确的时间差，并将时间差转换为秒
    return int(total_seconds)