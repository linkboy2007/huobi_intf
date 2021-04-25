#-*- coding:utf-8 -*-
import datetime 
import time
import json
import math
import requests
from websocket import create_connection
import gzip
import pandas as pd
from public.pubfunc import secNums
from requests.adapters import HTTPAdapter
import urllib3
from public.pubfunc import fmt_now_time, index_of_str
urllib3.disable_warnings()

class HuobiData(object):
    #货币的取数据接口 api.huobi.pro(需要翻墙) api.huobi.de.com[很慢],api.hadax.com[最快](国内地址)
    api_max = 2000
    socket_max = 300
    web_addr = 'api.hadax.com'
    #https://huobiapi.github.io/docs/spot/v1/cn/#d9d514d202 接口说明
    huobi_url = 'https://' + web_addr + '/market/history/kline?period=%s&size=%s&symbol=%s'
    #https://huobiapi.github.io/docs/spot/v1/cn/#k-2 接口说明
    huobi_web_socket = 'wss://' + web_addr + '/ws'

    def request_http_intf(self, params):
        # 获取request请求相关参数
        request_timeout = 5
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        s.keep_alive = False # 关闭多余连接, verify=False
        real_url = self.huobi_url % (params['period'], params['size'], params['symbol'])
        rsp = s.get(real_url, verify=False, timeout=request_timeout)
        ret_json = json.loads(rsp.text)
        if rsp.status_code == 200:
            if not 'err-code' in ret_json.keys():
                return True, ret_json['data']
            else:
                return False, ret_json["err-msg"]
        else:
            return False, rsp.text

    #period:1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
    def get_frequency(self, frequency):
        fre_list = ['1min', '5min', '15min', '30min', '60min', '4hour', '1day', '1mon', '1week', '1year']
        ret = frequency
        if frequency == '1d' or frequency == 'daily':
            ret = '1day'
        if frequency == '4h':
            ret = frequency + 'our'
        elif frequency == '1m' or frequency == '5m' or frequency == '15m' or frequency == '30m' or frequency == '60m':
            ret = frequency + 'in'
        if ret not in fre_list:
            ret = ''
        return ret

    def date_timestamp(self, dt):
        dt = dt + 28800 #加八个小时成为北京时间
        return dt

    def date_timestamp_int(self, dt):
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        timeStamp = timeStamp
        return timeStamp

    def date_timestamp_uxit(self, dt):
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        timeStamp = timeStamp + 28800 #加八个小时成为北京时间
        return str(timeStamp) + '000'

    def minNums(self, startTime, endTime):
        '''计算两个时间点之间的分钟数'''
        # 计算分钟数
        startTime2 = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime2 = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        seconds = (endTime2 - startTime2).seconds
        # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
        total_seconds = (endTime2 - startTime2).total_seconds()
        # 来获取准确的时间差，并将时间差转换为秒
        mins = math.ceil(total_seconds / 60)
        return int(mins)

    def calc_period(self, type_str, period, differ_value, count=0):
        ret = True
        index = index_of_str(period, type_str)
        p_num = int(period[:index])
        real_value = math.ceil(differ_value / p_num) + count
        if real_value > self.api_max:
            ret = False
        return ret

    #检查查询的日期范围和频率是否直接用api接口(3000条最大记录)就可以 true用api接口  false用web socket接口
    #period:1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
    def check_date_end(self, params, start_date, end_date, count):
        #默认是api接口
        ret = True
        period = params['period']
        curr_time = fmt_now_time()
        differ_min = 0
        differ_hour = 0
        differ_day = 0
        differ_week = 0
        differ_mon = 0
        differ_year = 0
        if count != None:
            differ_min = self.minNums(end_date, curr_time)
            differ_hour = math.ceil(differ_min / 60)
            differ_day = math.ceil(differ_min / (60 * 24))
            differ_week = math.ceil(differ_min / (60 * 24 * 7))
            differ_mon = math.ceil(differ_min / (60 * 24 * 30))
            differ_year = math.ceil(differ_min / (60 * 24 * 365))
            if 'min' in period:
                ret = self.calc_period('min', period, differ_min, count)
            elif 'hour' in period:
                ret = self.calc_period('hour', period, differ_hour, count)
            elif 'day' in period:
                ret = self.calc_period('day', period, differ_day, count)
            elif 'week' in period:
                ret = self.calc_period('week', period, differ_week, count)        
            elif 'mon' in period:
                ret = self.calc_period('mon', period, differ_mon, count)
            elif 'year' in period:
                ret = self.calc_period('year', period, differ_year, count)
        else:
            differ_min = self.minNums(start_date, curr_time)
            differ_hour = math.ceil(differ_min / 60)
            differ_day = math.ceil(differ_min / (60 * 24))
            differ_week = math.ceil(differ_min / (60 * 24 * 7))
            differ_mon = math.ceil(differ_min / (60 * 24 * 30))
            differ_year = math.ceil(differ_min / (60 * 24 * 365))
            if 'min' in period:
                ret = self.calc_period('min', period, differ_min)
            elif 'hour' in period:
                ret = self.calc_period('hour', period, differ_hour)
            elif 'day' in period:
                ret = self.calc_period('day', period, differ_day)
            elif 'week' in period:
                ret = self.calc_period('week', period, differ_week)        
            elif 'mon' in period:
                ret = self.calc_period('mon', period, differ_mon)
            elif 'year' in period:
                ret = self.calc_period('year', period, differ_year)            
        return ret

    #web socket请求数据，做多得到300条数据
    def web_socket_req(self, params, start_date_str, end_date_str, count):
        ret = False
        df_ret = None
        ws = None
        try:
            ws = create_connection(self.huobi_web_socket)
            # 订阅 KLine 数据 market.$symbol$.kline.$period$
            symbol = params['symbol']   #币种
            period = params['period']   #频率
            #每次最多返回300条
            if count != None:
                end_date = self.date_timestamp_int(end_date_str)
                tradeStr = """{"req":"market.%s.kline.%s", "id":"idmp", "to":%s}""" % (symbol, period, end_date)
            else:
                start_date = self.date_timestamp_int(start_date_str)
                end_date = self.date_timestamp_int(end_date_str)
                tradeStr = """{"req":"market.%s.kline.%s", "id":"idmp", "from":%s, "to":%s}""" % (symbol, period, start_date, end_date)
            if ws != None:
                ws.send(tradeStr)
                while(1):
                    compressData = ws.recv()
                    result = gzip.decompress(compressData).decode('utf-8')
                    if result[:7] == '{"ping"':
                        ts = result[8:21]
                        pong = '{"pong":' + ts + '}'
                        ws.send(pong)
                        ws.send(tradeStr)
                    else:
                        res = json.loads(result)
                        if not 'err-code' in res.keys():
                            ret = True
                            df_ret = res['data']
                        else:
                            ret = False
                            df_ret = res["err-msg"]
                        return          
        except Exception as e:
            df_ret = repr(e)
            print('error:' + repr(e))
        finally:
            return ret, df_ret

    #字段名称	数据类型	描述
    #id	long	调整为新加坡时间的时间戳，单位秒，并以此作为此K线柱的id
    #amount	float	以基础币种计量的交易量
    #count	integer	交易次数
    #open	float	本阶段开盘价
    #close	float	本阶段收盘价
    #low	float	本阶段最低价
    #high	float	本阶段最高价
    #vol	float	以报价币种计量的交易量
    def get_price(self, security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False,
                  fq='pre', count=None):
        ret = False
        err = ''
        df_ret = pd.DataFrame()
        try:
            #start_date和count不能同时有值
            if start_date != None and count != None:
                df_ret = pd.DataFrame()
                err = 'start_date和count不能同时有值'
                return
            if start_date == None and count == None:
                df_ret = pd.DataFrame()
                err = 'start_date和count不能同时为空'
                return
            #end_date一定不能为空
            if end_date == None:
                df_ret = pd.DataFrame()
                err = 'end_date不能为空'
                return
            if security == '':
                df_ret = pd.DataFrame()
                err = 'security不能为空'
                return
            security = security.replace('.', '')
            #日期格式,如果有秒，截取掉，只有年月日加时分
            if start_date != None:
                if len(start_date) > 19:
                    start_date = start_date[:19]
                elif len(start_date) == 10:
                    start_date = start_date + ' 00:00:00'
            if end_date != None:
                if len(end_date) > 19:
                    end_date = end_date[:19]
                elif len(end_date) == 10:
                    end_date = end_date + ' 00:00:00'                
            period = self.get_frequency(frequency)
            if period == '':
                df_ret = pd.DataFrame()
                err = 'frequency参数不正确'
                return
            size = self.api_max
            if period == '1min':
                size = 100 #分钟线写死为100条
            params = {
                'period' : period,
                'size' : size,
                'symbol' : security
            }
            #api接口最多每次只能请求2000条数据，先检查数据到现在是否2000条数据能查询到，如果不能调用websocket接口(300条)
            is_api = self.check_date_end(params, start_date, end_date, count)
            if is_api:
                if count != None:
                    if count > self.api_max:
                        df_ret = pd.DataFrame()
                        err = 'count大于最大的数量2000条'
                        return
                ret, ret_data = self.request_http_intf(params)
            else:
                if count != None:
                    if count > self.socket_max:
                        df_ret = pd.DataFrame()
                        err = 'count大于最大的数量300条'
                        return
                ret, ret_data = self.web_socket_req(params, start_date, end_date, count)
            if ret:
                df = pd.DataFrame(ret_data, columns=['id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count'])
                df.rename(columns={'id':'date', 'amount':'money', 'vol':'volume'}, inplace=True)
                #新加坡时区和北京时区都是东八时区，时间戳加8小时
                df['date'] = df['date'].apply(lambda x: self.date_timestamp(x))
                #按时间正序排列
                if is_api:
                    df = df.iloc[::-1]
                df.set_index('date', inplace=True)
                df.index.name = ''
                if not df.empty:
                    if count != None:
                        df.index = pd.to_datetime(df.index, unit='s')
                        df_ret = df[:end_date]
                        df_ret = df_ret.tail(count)
                        ret = True
                    else:
                        df.index = pd.to_datetime(df.index, unit='s')
                        df_ret = df[start_date:end_date]
                        ret = True
            else:
                err = ret_data
        except Exception as e:
            print('error=', repr(e))
            err = repr(e)
        finally:
            return ret, err, df_ret

    #得到缓存的1min数据,30秒内的数据可用
    #new_price_dict数据结构 {'btc.usdt': [54812.38, '2021-04-20 12:26:12'], 'doge.usdt': [0.402754, '2021-04-20 12:26:12']}
    def get_cache_min(self, code, end_date, new_price_dict):
        ret = False
        df_ret = pd.DataFrame()
        err = None
        try:
            if code in new_price_dict:
                data_list = new_price_dict[code]
                #请求的时间和缓存里的时间不能超过30秒 
                # get_price() 在返回价格的时候，先判断字典中最新价格是否在30秒内,如果是，直接用
                seconds = secNums(data_list[1], end_date)
                if abs(seconds) < 30:
                    print(code + '从缓存里取得数据', '缓存里的时间:' + data_list[1], '请求的时间:' + end_date)
                    df_ret = pd.DataFrame(pd.DataFrame([{'date': self.date_timestamp_uxit(data_list[1]), 'close':data_list[0]}]))
                    df_ret.set_index('date', inplace=True)
                    df_ret.index.name = ''
                    ret = True
        except Exception as e:
            err = repr(e)
            print('error:' + repr(e))
        finally:
            return ret, err, df_ret