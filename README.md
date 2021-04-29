# huobi_intf

提供火币网的实时行情服务器(支持火币网所有交易对的实时行情)，自带API缓存，可用于实盘交易和模拟回测。
行情数据，是一切量化交易的基础，可以获取1min、60min、4hour、1day等数据。数据能进行缓存，可以在多个币种，多个时间段查询的时候，查询速度依然很快。
服务框架采用基于强大的异步网络库tornado

### 功能特点：
* 为什么要用独立的行情服务器，直接调用火币的行情API不行吗？( https://github.com/mpquant/huobi_hq 我们另外一个项目，直接调用火币行情api的封装) 
  火币行情服务器比较慢，尤其在国内被墙，无法访问，尤其多个策略运行，一次需要获取多个币种数据做实时指标计算的时候，慢的让你怀疑人生，无法满足实盘要求，所以必须架设独立的行情服务器

* 自带Redis接口缓存，重复的历史日线，4小时线等数据获取一次即被缓存，下次策略再取得时候直接返回，速度加速上百倍  

* 完美包装火币的行情API,行情服务对外只简洁到一个get_price()函数，可以实时获取火币所有交易对实时行情，包括按天，4小时，1小时，15分钟，5分钟，1分钟的实时行情

* 历史行情支持从当前时间往前推3000条，和历史任意时间200条的数据 (需要历史任意时间3000以上条可以联系下面微信）

* 在本行情服务器基础上完全内存版本的本地历史行情服务器，用来做策略回测，调参等 (感兴趣的可以联系下面微信）

* 最简函数调用 get_price(security, start_date=None, end_date=None, count=None, frequency='1d', fields=['open','close', 'low', 'high']) 具体看下面例子，懂的自然能看懂

* 行情服务器编程语言是python,采用高性能异步网络框架tornado做WebApi, 标准json返回，所有语言都能方便调用

* 经过半年的运行，已经是非常稳定的版本，可以直接用在实盘生成环境

* 针对高频交易，每秒都要更新价格那种，可以联系最下面微信，我们提供分布式多端密集更新方案，来满足秒级别行情的要求

* 稳定，可靠，及时的行情服务器是高波动率数字货币量化交易的基础实施,我们全部开源出来，希望能帮助到大家

### 系统架构图：


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

#日线的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='1d')

#4小时的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='4h')

#1小时的数据获取
df = get_price('btc.usdt', end_date='2021-04-25 18:56:23', count=10, frequency='60m')

```

## btc的1分钟线
![btc1min](/img/btc_1min.png)

## btc日线
![btc日线](/img/btc_1day.png)
 
## btc的4小时线
![btc小时线](/img/btc_4hour.png)


2、显示btc和eth的实时close价格的接口info，返回dataframe的格式

![test](/img/test.png)

3、intf_test.py里有调用这个两个接口的例子

----------------------------------------------------

## 巴特量化(BestQuant)：数字货币 股市量化工具 行情系统软件，BTC虚拟货币量化交易策略开发 自动化交易策略运行
----------------------------------------------------

![加入群聊](/img/qrcode.png) 
