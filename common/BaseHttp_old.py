import time
from turtle import Vec2D
# from common.
import requests
from requests.adapters import HTTPAdapter

r = requests.Session()
r.mount('http://', HTTPAdapter(max_retries=3))
r.mount('https://', HTTPAdapter(max_retries=3))

class BaseHttp(object):
    def __init__(self,is_uc = 0 ,env=None,language=None, is_ssl=True, third_math=1):
        """
        host = bcs-app-service.sdp.101.com
        version = v0.1
        """
        self.host = "bcs-app-service.sdp.101.com"
        self.port = ''
        self.version = "v0.1"
        self.env = env
        self.language = language
        self.time_out_line = 15
        self.is_ssl = is_ssl
        self.third_math = third_math

        # 2.设置默认的header
        self.header = dict()
        self.header['Content-Type'] = 'application/json'
        self.header['Accept-Language'] = 'zh-CN,zh;q=0.8'
        try:
            self.mt_auth = MtAuth(env=self.env,sdp_app_id=self.sdp_app_id,user_id=self.user,org_name=self.org_name,password=self.password)
            if self.third_math==1:
                self.header['nd-meeting-token'] = self.mt_auth.get_meeting_token()["token"]
        except Exception as e:
            print(e)
        print("get nd-meeting-token:")


    def get_uri(self, url, version=None):
        if version == '' or version is None:
            if self.version == '' or self.version is None:
                return "/" + url
            else:
                return '/' + str(self.version) + '/' + url
        else:
            return "/" + str(version) + "/" + url

    def get_url(self, url, version=None):
        ssl_method = "https"
        if not self.is_ssl:
            ssl_method = "http"
        print(ssl_method, self.host, self.port, self.get_uri(url=url, version=version))
        print("%s://%s:%s%s" % (ssl_method, self.host, self.port, self.get_uri(url=url, version=version)))
        if self.port and len(self.port) > 0:
            return "%s://%s:%s%s" % (ssl_method, self.host, self.port, self.get_uri(url=url, version=version))
        else:
            return "%s://%s%s" % (ssl_method, self.host, self.get_uri(url=url, version=version))

    def post(self, url, json=None, data=None, version=None, if_uc_auth=False):
        url = self.get_url(url, version)
        if if_uc_auth:
            self.header["Authorization"] = self.mt_auth.get_auth(method="POST", url=url)
        start_time = time.time()
        response = r.post(url=url, json=json, data=data, headers=self.header, verify=False, timeout=self.time_out_line)
        end_time = time.time()
        self.print_detail(method="post", url=url, response=response, body=json)
        print('请求耗时：{}秒'.format(end_time - start_time))
        return response