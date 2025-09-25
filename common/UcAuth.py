"""
这个做mac token 的接口请求

"""

import hashlib
import json
import requests
import hmac
import base64
import time
import random
import string
from urllib.parse import urlsplit

default_time_out = 20000
appId = "09aad54e0c85495ab1d0366ac2473938"

class UcAuth:
    access_token = ''
    mac_key = ''
    response_entity = {}
    uc_service_urls = {
        "ol": "https://aqapi.101.com",
        "pre": "https://ucbetapi.101.com"
    }

    def __init__(self, user_id='336915', password = 'momocll343', org_name="nd", env="ol"):
        super().__init__()
        self.userId = user_id
        self.pwd = password
        self.org_name = org_name
        self.uc_service_url = UcAuth.uc_service_urls[env]

    def login_in(self):
        url = '%s/v0.93/tokens' % self.uc_service_url
        print(url)
        formdata = {
            "login_name": self.userId,
            "password": self.__pwd_encrypt(self.pwd),
            "org_name": self.org_name,
        }
        headers = {'User-agent': 'DYZB/1 CFNetwork/808.2.16 Darwin/16.3.0', 'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        response = requests.post(
            url, json=formdata, headers=headers, timeout=default_time_out, proxies=None)
        UcAuth.response_entity = json.loads(response.text)
        UcAuth.access_token = UcAuth.response_entity['access_token']
        UcAuth.mac_key = UcAuth.response_entity['mac_key']
        print(f"UcAuth.mac_key = {UcAuth.mac_key}")
        print(UcAuth.access_token)


    def __pwd_encrypt(self, password):
        """
        混淆MD5加密
        :param password:
        :return:
        """
        content = password + "\xa3\xac\xa1\xa3" + "fdjf,jkgfkl"
        buffer = content.encode("iso-8859-1")
        # 创建md5对象
        hl = hashlib.md5()
        hl.update(buffer)
        hashBytes = hl.hexdigest()
        return hashBytes

    @staticmethod
    def auth_request(method, url, json_body=None, header=None, form_data=None):
        headers = UcAuth.get_uc_headers(method.upper(), url, header)
        response = ''
        if method.upper() == 'GET':
            response = requests.get(
                url, headers=headers, timeout=default_time_out, proxies=None)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=json_body, data=form_data,
                                    headers=headers, timeout=default_time_out, proxies=None)
        elif method.upper() == 'POST':
            response = requests.post(url, json=json_body, data=form_data,
                                     headers=headers, timeout=default_time_out, proxies=None)
        # print(f"response status ={response.status_code}")
        # print(f"response text ={response.text}")
        # result = json.loads(response.text)
        result = response
        print(response.text)
        return result

    @classmethod
    def get_uc_headers(cls, method, url, header=None):
        auth = UcAuth.get_auth(method.upper(), url)
        headers = {
            'User-agent': 'DYZB/1 CFNetwork/808.2.16 Darwin/16.3.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth}
        if header is not None:
            headers.update(header)
        print(f"headers:/n {headers}")
        return headers

    @classmethod
    def __hmac(cls, mac_key, nonce, http_method, path_query, host):
        '''
         签名算法：hmac-sha-256
        :param mac_key:qFkgnEyPlw
        :param nonce:1419408940756:afdgf454
        :param http_method:POST
        :param path_query:
        :param host:
        :return: 计算出的签名值：mac:tpyIZvChUkgBj3IcEqKigxiWXux/3ASeP47hbaT+YlI=
        '''
        # nonce = '1419408940756:afdgf454'
        # path_query = '/v0.3/tokens/be38bc32-e5f9-421f-8da6-606cbfd2253e/actions/valid'
        # host = '101uccenter.web.sdp.99.com'
        # http_method = 'POST'
        # macKey = 'qFkgnEyPlw'
        content = "%s\n%s\n%s\n%s\n" % (nonce, http_method, path_query, host)
        secret = mac_key.encode("iso-8859-1")
        message = content.encode("iso-8859-1")
        s_hmac = hmac.new(secret, message, digestmod=hashlib.sha256).digest()
        encodestr = base64.b64encode(s_hmac)
        return encodestr.decode('ascii')

    @classmethod
    def __get_nonce(cls):
        '''
        时间戳(精确到毫秒) + ":" + '随机码'(8位)'；5分钟后失效，且只能使用一次(随机码可以包含大小写字母和数字)
        :return:
        '''

        def nowTime(): return str(round(time.time() * 1000))

        nonce = nowTime() + ':' + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return nonce

    @classmethod
    def get_auth(cls, method, url):
        """
        这个就是获取mac token 的

        MAC id="7F938B205F876FC3E6617B29946021A7BEDC5EADC5BCAA1208899EA86275EAA591DF11B6F3061BC56D7B662D9F99B9BF",
        nonce="1752481382886:PVNBM2TO",
        mac="vTwdKsh6QO2MUkSOZ4t3Ag58HRj3JsHyUfvlSrfSmf0="

        :param method:
        :param url:
        :return:
        """
        parsed_url = urlsplit(url)
        host = parsed_url.netloc
        path_and_query = ''
        if (parsed_url.query != ''):
            path_and_query = parsed_url.path + '?' + parsed_url.query
        else:
            path_and_query = parsed_url.path
        nonce = cls.__get_nonce()
        mac = cls.__hmac(cls.mac_key, nonce, method, path_and_query, host)
        auth = "MAC id=\"%s\",nonce=\"%s\",mac=\"%s\"" % (
            cls.access_token, nonce, mac)
        print(auth)
        return auth

    def get_user_info(self, usr_id):
        """
        获取用户信息
        :param usr_id:
        :return:
        """
        url = '%s/v0.93/users/%s?realm=uc.sdp.nd' % (self.uc_service_url,usr_id)
        print(url)
        return UcAuth.auth_request('GET', url)

if '__main__' == __name__:
    # ucAuth = UcAuth(env="pre",user_id="666658",password="Qa123456",org_name="ndtest")
    ucAuth = UcAuth(env="ol", user_id="336915", password="momocll343", org_name="nd")
    ucAuth.login_in()
    ucAuth.get_user_info(usr_id="336915")
    # print(json.dumps(ucAuth.get_user_info("336915"),indent=4, ensure_ascii=False))