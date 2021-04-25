#-*- coding:utf-8 -*-
from modules.huobi_intf import *
from modules.update_min import *

modules_urls = [
    (r"/get_price", GetHuobiPrice),
    (r"/info", Info)
]