# ipidea-proxy

Python library for ipidea proxy service API

![Github Checker](https://github.com/pinclr/ipidea-proxy/actions/workflows/pytest.yml/badge.svg?branch=main)
[![Documentation Status](https://readthedocs.org/projects/ipidea-proxy/badge/?version=latest)](https://ipidea-proxy.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://pepy.tech/badge/ipidea-proxy)](https://pepy.tech/project/ipidea-proxy)

## 使用客户端

### 0. 安装

通过pip安装ipidea-proxy的python客户端

```shell
$ pip install --upgrade ipidea-proxy
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting ipidea-proxy
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/3a/65/b537feb63f22ce9453600cd49fbf1a230df6914c1ba133ed91efb1fa9a53/ipidea_proxy-0.5.0-py3-none-any.whl (7.8 kB)
Installing collected packages: ipidea-proxy
Successfully installed ipidea-proxy-0.5.0
```

### 1. 获取UID和APPKEY

登录用户Profile

https://www.ipidea.net/ucenter/

然后访问API文档链接，从页面上获取UID和APPKEY

https://www.ipidea.net/ipidea-api.html#001

### 2. 设置环境变量

通过上面获取的UID和APPKEY，设置到以下的环境变量。客户端会自动从该环境变量读取。

```shell
export IPIDEA_UID=xxx
export IPIDEA_APPKEY=xxx
```

### 3. 初始化客户端

```shell
from ipidea_proxy import IpideaProxy

# 通过环境变量设置UID和APPKEY
# 如果UID和APPKEY已经通过环境变量设置，可以这样初始化客户端
ipp = IpideaProxy()

# 通过参数设置UID和APPKEY
ipp = IpideaProxy(uid='xxxx', appkey='xxxxxx')

```

### 4. 使用客户端

#### 4.1 白名单
##### 4.1.1 设置IP到白名单

```shell
# 添加本机公网IP到白名单
ipp.add_whitelist()

# 添加2.3.4.5到白名单
ipp.add_whitelist('2.3.4.5')

# 添加多个IP到白名单（e.g. '2.3.4.6','2.3.4.7')
ipp.add_whitelist('2.3.4.6,2.3.4.7')
```

##### 4.1.2 查看已设置的白名单

```shell
# 查看完整白名单列表
ipp.list_whitelist()
```

##### 4.1.3 从白名单中删除IP

```shell
# 从白名单中删除指定IP
ipp.delete_whitelist('2.3.4.5')

# 从白名单中删除本机对应公网IP
ipp.delete_whitelist()
```

#### 4.2 流量
##### 4.2.1 获取剩余流量

```shell
# 获取当前账号剩余流量
ipp.get_remaining_quota()
```
##### 4.2.2 流量设置预警

```shell
# 设置日预警值 101 并通知到指定手机号 188-8888-8888
ipp.set_alarm_threshold('18888888888','101',0,0)

# 设置流量自停
ipp.set_alarm_threshold('18888888888','101',1,0)

# 开启预警
ipp.set_alarm_threshold('18888888888','101',0,1)
```

##### 4.2.3 查看主账户流量使用

```shell
# 查看主账号流量使用情况 (在输入函数中填写具体的起始时间)
ipi.get_main_account_usage()
```

##### 4.2.4 查看认证账户流量
```shell
# 查看账户666666的使用流量 (在输入函数中填写具体的起始时间)
ipi.get_sub_account_usage('666666')
```

## API Reference

https://www.ipidea.net/ipidea-api.html#001

