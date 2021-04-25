#-*- coding:utf-8 -*-
import json
from datetime import datetime

def packet_result(params, func_name, json_file, err=''):
    """
    包装返回结果
    :param params:
    :param func_name:
    :param json_file:
    :return:
    """
    dct = json.loads(json_file)
    if err == '':
        result = json.dumps({
            "params": params,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "func_name": func_name,
            "return_result": dct,
            "records_count": len(dct)
        })
    else:
        result = json.dumps({
            "params": params,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "func_name": func_name,
            "return_result": dct,
            "records_count": len(dct),
            "errmsg": err
        })        
    return result