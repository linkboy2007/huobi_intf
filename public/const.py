#-*- coding:utf-8 -*-

from enum import Enum, unique

'''
api_json:接口返回数据的默认格式
======================================================
'''
api_json = {}
'''
/* code:执行状态码
*  0 成功
*  403 无权限 前台将弹出二次登录确认框
*  404 资源不存在
*  500 未确定内部错误
*  200-300 自定义状态码
*/
'''
api_json["code"] = 0 
API_SUCC = 0              #成功
API_NO_PERMISSION = 403   #无权限
API_RES_NOT_EXIST = 404   #资源不存在
API_INTERNAL_ERROR = 500  #未确定内部错误
API_TIME_ERROR = 501      #时间错误
API_SMS_ERROR = 502       #短信账号正在审核

'''
/* msg:错误信息
*  仅在状态码500有效
*  其余非0状态码，框架将读取i18n相应状态码配置信息显示
*/
'''
api_json["msg"] = ''
'''
/* result:结果数据 仅在状态码0有效
*  可为任意有效数据，字符串、数字、数组、json等
*/
'''
api_json["result"] = None

'''
#需要返回报表数据时的result_json格式
=========================================================
'''
result_json = {}
result_json["total"] = 0  #满足此次查询条件的数据总数
result_json["items"] = None #此次查询数据列表，json数组

#默认一页有多少行
default_linesperpage = 20

#操作员Token间隔时间8小时 单位:秒 28800秒
TOKEN_TIME = 8 * 60 * 60;

#客户端时间与服务器时间的最大差值 5分钟
TIME_DIFF = 5 * 60

#下边是常量字符串定义
MP_TIMESTAMP = 'MP-TIMESTAMP'           #接口发过来的时间戳
MP_ACCESS_TOKEN = 'MP-ACCESS-TOKEN'     #接口发过来的token
MP_SPEC_ID = 'MP-SPEC-ID'               #接口发过来的用户公司编号
MP_FRONT_TYPE = 'MP-FRONT-TYPE'         #接口发过来的软件标识pc\app
MP_SIG = 'MP-SIG'                       #接口发过来的数字签名串

PSW123456 = 'e10adc3949ba59abbe56e057f20f883e'  #123456
PSWBLANK = 'd41d8cd98f00b204e9800998ecf8427e'   #空白的md5
MP_KEY = 'e10adc3949ba59abbe56e057f20f883e' #数字签名校验码


#下边会定义一些枚举 不要出现野数字

#token检测对应的返回值
@unique
class TokenCheck(Enum):
    TOKEN_OK = 0            #token检测正确
    TOKEN_NO_EXIST = 1      #token不存在
    TOKEN_EXPIRE = 2        #token已过期
    TOKEN_USER_NOAUTHS = 3  #token对应用户的权限不足
    
#判断字段名称是否符合命名规范的返回值
@unique
class FieldCheck(Enum):
    Field_OK = 0            #正确
    Field_DIGIT = 1         #纯数字
    Field_NOCHAR = 2        #非法字符
    
@unique
class CostType(Enum):
    ct_new = 0            #新的股票数据
    ct_exist = 1          #存在的股票数据