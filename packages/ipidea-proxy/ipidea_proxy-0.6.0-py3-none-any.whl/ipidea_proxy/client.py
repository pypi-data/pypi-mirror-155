""" Client Library for IPIDEA Proxy Service API
"""

import requests
import time
import os

class IpideaProxy(object):

  def __init__(self, uid='', appkey='') -> None:
    #
    # get the uid and appkey from https://www.ipidea.net/ipidea-api.html#001
    # after signed in from https://www.ipidea.net/userLogin
    #
    if uid:
      self.uid = uid
    else:
      self.uid = os.environ.get('IPIDEA_UID')

    if appkey:
      self.appkey = appkey
    else:
      self.appkey = os.environ.get('IPIDEA_APPKEY')

    self.apibase = 'https://api.ipidea.net/api/open/'

  def auth(self, uid, appkey):
    """auth the client when the client is instantiated without auth info
    """
    self.uid = uid
    self.appkey = appkey

  """whitelisting APIs
  """

  #添加白名单：
  def add_whitelist(self, white_ips):
    url = f'{self.apibase}white_add'

    params = {
      'uid': self.uid,
      'appkey': self.appkey,
      'white_ips': white_ips
    }

    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data
    
  #查找白名单：
  def list_whitelist(self):
    url = f'{self.apibase}white_list'

    params = {
      'uid':self.uid,
      'appkey':self.appkey
    }

    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data
    
  #删除白名单:
  def delete_whitelist(self, white_ips):
    url = f'{self.apibase}white_del'

    params = {
      'uid':self.uid,
      'appkey':self.appkey,
      'white_ips':white_ips
    }

    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data

  
  """authentication APIs
  """

  def add_auth_account(self):
    pass

  def patch_auth_account(self):
    pass

  def delete_auth_account(self):
    pass


  """flow APIs
  """

    #获取剩余流量
  def get_remaining_quota(self):
    url = f'{self.apibase}flow_left'
        
    params = {
        'uid':self.uid,
        'appkey':self.appkey
    }

    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data
    
  #流量预警设置
  def set_alarm_threshold(self, phone, flow_upper_limit, operate, status):
    url = f'{self.apibase}flow_warning_set'
        
    params = {
      'uid':self.uid,
      'appkey':self.appkey,
      'phone':phone,
      'flow_upper_limit':flow_upper_limit,
      'operate':operate,
      'status':status
    }
        
    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data
    
    #查看主账户流量使用：
  def get_main_account_usage(self):
    url = f'{self.apibase}flow_use_record'
      
    print('Please input start_date and end_date in YYYY-MM-DD HH:MM:SS format')
    start_time = input('Start Date Input:')
    end_time = input('End Date Input:')
    
    start_date = time.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    end_date = time.strptime(end_time,'%Y-%m-%d %H:%M:%S')
    input_start = int(time.mktime(start_date))
    input_end = int(time.mktime(end_date))

    params = {
      'uid':self.uid,
      'appkey':self.appkey,
      'start_time':input_start,
      'end_time':input_end
    }
        
    r = requests.Session()
    r0 = r.post(url=url,params=params)
    try:
        data = r0.json()
    except Exception as e:
        raise(e)

    return data
    
  #查看认证账户流量：
  def get_sub_account_usage(self, sub_id):
    url = f'{self.apibase}flow_proxy_account_use_record'

    print('Please input start_date and end_date in YYYY-MM-DD HH:MM:SS format')
    start_time = input('Start Date Input:')
    end_time = input('End Date Input:')
    
    start_date = time.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    end_date = time.strptime(end_time,'%Y-%m-%d %H:%M:%S')
    input_start = int(time.mktime(start_date))
    input_end = int(time.mktime(end_date))
        
    params = {
      'uid':self.uid,
      'appkey':self.appkey,
      'start_time':input_start,
      'end_time':input_end,
      'sub_id':sub_id
    }
    
    r = requests.Session()
    r0 = r.get(url=url,params=params)
    try:
      data = r0.json()
    except Exception as e:
      raise(e)

    return data

  """IP APIs
  """

  def datacenter_ip(self):
    pass

  def residential_ip(self):
    pass

  def get_datacenter_ip(self):
    pass

  def get_residential_ips(self):
    pass

  def get_residential_ips(self):
    pass


  """ordering APIs
  """

  def get_dynamic_flow_orders(self):
    pass

  def get_datacenter_ip_orders(self):
    pass

  def get_residential_ip_orders(self):
    pass


  """get IP addresses
  """
  def get_ip_address_from_auth_account(self, proxy_user, proxy_pass, proxy_addr='proxy.ipidea.io:2333', proxy_region=''):

    proxies = {
      'http': proxy_addr
    }

    if proxy_region != '':
      proxy_region = '-region-'+proxy_region
    proxy_pass = f"{proxy_user}-zone-custom{proxy_region}:{proxy_pass}"

    url = 'http://ipinfo.io'

    session = requests.Session()
    session.auth = (proxy_user, proxy_pass)

    res = session.get(url, proxies=proxies)
    try:
      data = res.json()
    except Exception as e:
      raise(e)

    return data

def get_ip_addresses_from_whitlisted_ip(self, nums=100, proto='http', format='json', region=''):
  # cap on 900
  if nums > 900:
    nums = 900
  if nums < 1:
    nums = 1

  API_BASE = 'api.proxy.ipidea.io/getProxyIp'
  if nums > 500:
    url = f'http://{API_BASE}?big_num={nums}&return_type={format}&lb=1&sb=0&flow=1&regions={region}&protocol={proto}'
  else:
    url = f'http://{API_BASE}?num={nums}&return_type={format}&lb=1&sb=0&flow=1&regions={region}&protocol={proto}'

  res = requests(url)

  try:
    data = res.json()
  except Exception as e:
    raise(e)

  return data
