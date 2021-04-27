# huobi_intf

提供火币网的获取数据的接口，可用于实盘交易和模拟交易
行情数据，是一切量化交易的基础，本封装用一个函数解决获取数字货币所有币种的实时行情
数据放入pandas中，剩下的如何使用，分析就是简单了！

### python的版本
●python >= 3.6

### 接口说明
1、get_price接口得到火币的币的数据，返回dataframe的格式

```python
code='btc.usdt'
print(code,'最新价格',get_last_price(code))
df=get_price(code,count=5,frequency='4h');      #1d:1天  4h:4小时   60m: 60分钟    15m:15分钟
print(df)
```

## btc日线
![btc日线](/img/btc_1day.png)
 
## btc的4小时线
![btc小时线](/img/btc_4hour.png)

2、显示btc和eth的实时close价格的接口info，返回dataframe的格式

```python
     币名称      close                 时间
1  btc.usdt  50115.19  2021-04-25 09:39:26
2  eth.usdt   2235.95  2021-04-25 09:39:27
```

3、intf_test.py里有调用这个两个接口的例子

```python
    df = get_price('btc.usdt', end_date=fmt_now_time(), count=1, frequency='1m', fields=['close'])
    print(df)
    df = get_info()
    print(df)
```

## 需安装第三方库
* requests
* pandas
* tornado
* websocket-client
 

----------------------------------------------------
### 巴特量化(BestQuant)：数字货币 股市量化工具 行情系统软件提供商
----------------------------------------------------

![加入群聊](/img/qrcode.png) 
