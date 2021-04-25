#-*- coding:utf-8 -*-
import json
import os
import datetime
import pandas as pd
from tornado.options import define, options
from public.rw_config  import rwcfg

define("port", type=int, default=9001)
define("debug", default="", type=bool)

r = rwcfg()#实例化配置文件读写类
options.port = int(r.read("server", "port", 9001))

#缓存的get_price数据
init_date = datetime.datetime.now().strftime("%Y-%m-%d")
coin_mem = {}

#缓存的币种列表,有时间，为了获取分钟线数据用的
coin_cache = {}
cache_date = datetime.datetime.now().strftime("%Y-%m-%d")

#最新价格字典
new_price_dict = {}