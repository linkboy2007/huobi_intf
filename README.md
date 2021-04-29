# huobi_intf

提供火币网的实时行情服务器(支持火币网所有交易对的实时行情)，自带API缓存，可用于实盘交易和模拟回测。
行情数据，是一切量化交易的基础，可以获取1min、60min、4hour、1day等数据。数据能进行缓存，可以在多个币种，多个时间段查询的时候，查询速度依然很快。
服务框架采用基于强大的异步网络库tornado

###功能特点：
* 完美包装火币的行情API,行情服务对外只简洁到一个get_price()函数，可以实时获取火币所有交易对实时行情

### 服务器启动说明
运行文件huobi_app.py启动服务，服务启动后就可以用程序调用所有的接口  
python3 huobi_app.py --port=8005  
启动成功后，在浏览器里输入`http://127.0.0.1:8005/info`，如果能出现下边的画面，说明启动成功了  
![info](/img/info.png)

### python的版本
* python >= 3.6

## 需安装第三方库
* requests
* pandas
* tornado
* websocket-client

安装时执行命令:pip install -r requirements.txt

### 接口说明
1、get_price接口得到火币的币的数据，返回dataframe的格式

```python
#1分钟的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=1, frequency='1m')
print(df)

#日线的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='1d')
print(df)

#4小时的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='4h')
print(df)

#1小时的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='60m')
print(df)

#取到btc和eth的实时分钟线数据
df = get_info()
print(df)
```

## btc的1分钟线
![btc1min](/img/btc_1min.png)

## btc日线
![btc日线](/img/btc_1day.png)
 
## btc的4小时线
![btc小时线](/img/btc_4hour.png)

## btc的60分钟线
![btc60min](/img/btc_60min.png)

2、显示btc和eth的实时close价格的接口info，返回dataframe的格式

![test](/img/test.png)

3、intf_test.py里有调用这个两个接口的例子

----------------------------------------------------
### 巴特量化(BestQuant)：数字货币 股市量化工具 行情系统软件提供商
----------------------------------------------------

![加入群聊](/img/qrcode.png) 
