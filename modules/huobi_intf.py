#-*- coding:utf-8 -*-
import tornado.gen
import tornado.ioloop
import tornado.web
import copy
from tornado.escape import json_decode
from public.basic_class import BaseHandle
from public.const import *
from public.pubfunc import *
from .jq_func import *
from modules.huobi_func import *

class GetHuobiPrice(BaseHandle):
    """通过火币网查询数字货币数据
    @api {post} /get_price 策略下单-通过火币网查询数字货币数据
    @apiVersion 1.0.0
    @apiGroup 策略系统
    @apiName  GetPrice
    @apiDescription 用于火币网查询数字货币数据

    @apiParam {string}    security         (必选)代码
    @apiParam {string}    start_date       (可选)格式同上, 开始时间, 不能和count同时存在,默认是'2015-12-31', 包含此日期. 分钟线格式为2020-01-05 15:00
    @apiParam {string}    end_date         (必选)格式同上, 结束时间, 默认是'2015-12-31', 包含此日期. 分钟线格式为2020-01-05 15:00
    @apiParam {string}    frequency        (必选)单位时间长度, 1d 日线数据, 1m 一分钟数据
    @apiParam {int}       count            (可选)end_date前count个数据，不能和start_date同时存在
    @apiParam {string}    fields           (可选)可查询字段为open,close,low,high,colume,money
    @apiParamExample {json} 参数事例:
    {
        "security": "510300.XSHG",
        "start_date": "2020-12-01",
        "end_date": "2020-12-01",
        "frequency": "1d",
        "fields":[
            "close",
            "open",
            "low",
            "high",
            "volume"
        ]
    }

    @apiSuccess {int}             code        内部错误500 执行成功0
    @apiSuccess {string}          msg         返回详情 code为500时有效
    @apiSuccess {json}            result      结果为None
    @apiSuccessExample {json} 成功时的返回数据:
    {
        "params": {
            "security": "510300.XSHG",
            "start_date": "2020-12-01",
            "end_date": "2020-12-01",
            "frequency": "1d",
            "fields":[
                "close",
                "open",
                "low",
                "high",
                "volume",
                "money"
            ]
        },
        "time": "2021-01-05 16:22:14",
        "func_name": "get_price",
        "return_result": {
            "2021-01-05": {
                "open": 5.321,
                "close": 5.433,
                "high": 5.445,
                "low": 5.305,
                "volume": 6228308.0,
                "money": 3349890560.0
            }
        },
        "records_count": 1
    }
    """    
    @tornado.gen.coroutine
    def post(self):
        result = {}         #初始化数据结果JSON   
        try:
            params = json_decode(self.request.body)
            #发现缓存里数据就取缓存里的数据
            freq_time = self.get_frequency(params['frequency'])
            curr_date = ''
            coin_md5 = ''
            if freq_time == '1day' or freq_time == '4hour' or freq_time == '60min':
                start_date = ''
                if 'start_date' in params.keys() and params['start_date'] != None:
                    if freq_time == '1day':
                        start_date = str(params['start_date'])[:10]
                    elif freq_time == '4hour':
                        e_dt = str(params['start_date'])
                        e_date = e_dt[:10]
                        e_time = str(int(e_dt[11:13]) // 4).zfill(2)
                        start_date = e_date + e_time
                    elif freq_time == '60min':
                        start_date = str(params['start_date'])[:13]
                count = ''
                if 'count' in params.keys() and params['count'] != None:
                    count = str(params['count'])
                end_date = ''
                if 'end_date' in params.keys():
                    if freq_time == '1day':
                        end_date = str(params['end_date'])[:10]
                    elif freq_time == '4hour':
                        e_dt = str(params['end_date'])
                        e_date = e_dt[:10]
                        e_time = str(int(e_dt[11:13]) // 4).zfill(2)
                        end_date = e_date + e_time
                    elif freq_time == '60min':
                        end_date = str(params['end_date'])[:13]
                param_str = params['security'] + freq_time + start_date + end_date + count + ''.join(params['fields'])
                coin_md5 = getmd5(param_str)
                print(coin_md5, param_str)
                curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
                if curr_date == dbc.init_date:
                    if coin_md5 in dbc.coin_mem.keys():
                        print('get', curr_date, dbc.init_date)
                        json_file = dbc.coin_mem[coin_md5]
                        result = packet_result(params, "get_price", json_file)
                        return
            elif freq_time == '1min':
                #每次get_price的时候，把币种类加入一个字典，为了接口get_pair准备缓存数据，日期为服务器当期时间
                code = params['security']
                dbc.coin_cache[code] = fmt_now_date()
                print('get_price缓存币的数据:', dbc.coin_cache)
            col_name = copy.deepcopy(params['fields'])
            ret = False
            err = ''
            df = pd.DataFrame()
            huobi_data = HuobiData()
            if freq_time == '1min':
                #先取缓存数据，取不到再从火币取数据
                ret, err, df =  huobi_data.get_cache_min(params['security'], str(params['end_date']), dbc.new_price_dict)
                if not ret:
                    ret, err, df = huobi_data.get_price(**params)
                    if ret:
                        if not df.empty:
                            #用从火币获取获取的数据更新缓存里的数据,如果请求的日期和现在的日期相差在30秒内
                            curr_date = fmt_now_time()
                            seconds = secNums(str(params['end_date']), curr_date)
                            if abs(seconds) < 30:
                                print('相差在30秒内,更新数据缓存......')
                                code = params['security']
                                data_list = []
                                data_list.append(df['close'][0])
                                data_list.append(curr_date)
                                dbc.new_price_dict[code] = data_list
            else:
                ret, err, df = huobi_data.get_price(**params)
            if ret:
                if not df.empty:
                    df = df[col_name]
                    json_file = df.to_json(orient='index', force_ascii=False)
                    if freq_time == '1day' or freq_time == '4hour' or freq_time == '60min':
                        curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        print('set', curr_date, dbc.init_date)
                        if curr_date != dbc.init_date:
                            print('日期发生变化，进行值的修改') 
                            dbc.init_date = curr_date
                            dbc.coin_mem = {}
                        dbc.coin_mem[coin_md5] = json_file    
                else:
                    json_file = '{}'
                result = packet_result(params, "get_price", json_file)
            else:
                json_file = '{}'
                result = packet_result(params, "get_price", json_file, err)
        except Exception as e:
            json_file = '{}'
            err = repr(e)
            result = packet_result({}, "get_price", json_file, err)
        finally:
            self.finish(result)   # finish JSON功能

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