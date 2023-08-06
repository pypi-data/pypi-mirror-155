Kong 网关 HMAC 鉴权 Python SDK
------------------------------

介绍
----

Kong 网关的的 Python 客户端
SDK，同样适用于移植到APISIX的HMAC鉴权，相关介绍：https://zhang.ge/5159.html

快速上手
--------

SDK 安装
~~~~~~~~

.. code:: shell

   pip install kong-hmac

网关鉴权
^^^^^^^^

.. code:: python

   import requests
   from kong_hmac import HmacAuth

   if __name__ == "__main__":
       # 根据实际情况修改
       USERNAME = "demo"
       SECRET = "ujHURnS5Wlb***********QmJdkDMEep"
       API_URL = "http://xxx.xxx.com/hmac_test"
       param = {"xxx": {"xxxx": "xxx"}}

       # 方式一：在初始化class的时候设置账号密钥
       hmac_auth = HmacAuth(hmac_user=USERNAME, hmac_secret=SECRET)
       headers = hmac_auth.get_auth_headers()

       # 方式二：在生成头部的时候设置账号密钥
       # hmac_auth = HmacAuth()
       # headers = hmac_auth.get_auth_headers(hmac_user=USERNAME, hmac_secret=SECRET)

       resp = requests.post(url=API_URL, json=param, headers=headers)

       if resp.status_code in [200, 201]:
           print(headers)
           exit("Test OK!")

       else:
           print(headers)
           print(resp.text)
           exit("Test Failed!")
