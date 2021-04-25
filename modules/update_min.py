#-*- coding:utf-8 -*-
import tornado.gen
import tornado.ioloop
import tornado.web
from public.basic_class import BaseHandle
from public.const import *
from public.pubfunc import *
from .jq_func import *
from modules.huobi_func import *

#info接口,返回网页格式的币(btc和eth)的数据
class Info(BaseHandle):
    @tornado.gen.coroutine
    def post(self):
        result = ''
        df = pd.DataFrame()
        try:
            huobi_data = HuobiData()
            coin_dict = ['btc.usdt', 'eth.usdt']
            table_lsit = []
            for code in coin_dict:
                curr_date = fmt_now_time()
                params = { 
                    "security": code,
                    "end_date": curr_date,
                    "count": 1,
                    "frequency": "1m",
                    "fields":[
                        "close"
                    ]
                }
                close_price = 0
                ret, err, df = huobi_data.get_price(**params)
                if ret:
                    if not df.empty:
                        close_price = df['close'][0]
                code_list = []
                code_list.append(code)
                code_list.append(close_price)
                code_list.append(curr_date)
                table_lsit.append(code_list)
            df = pd.DataFrame(table_lsit, columns = ['币名称', 'close', '时间'])
            df.index += 1
            df.index.name = ''
            json_file = df.to_json(orient='index', force_ascii=False)
            result = packet_result({}, "info", json_file)
        except Exception as e:
            print(repr(e))
        finally:
            self.finish(result)   # finish JSON功能