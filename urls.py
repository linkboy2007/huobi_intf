#-*- coding:utf-8 -*-
from public.basic_class import BaseHandle
from modules.modules_url import modules_urls

err404_urls = [
    (r".*", BaseHandle)
]  

urls = modules_urls + \
       err404_urls #必须最后一个 

#print(urls)