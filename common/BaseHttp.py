# -*- coding: utf-8 -*-
"""
@author: Lily
@contact: 你的邮箱
@created: 2025/9/18
"""
import requests
import logging
import json
from time import sleep
from typing import Dict,Any,Optional,Union
from requests.exceptions import RequestException, Timeout

#设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class BaseHttp:
    """HTTP 客户端类，封装常见的 HTTP 请求操作"""
    def __init__(self,base_url:str ="",timeout:int = 600,max_retries:int = 3,env=None,is_ssl= True,version:str=""):
        """
        初始化 HTTP 客户端

        Args:
            base_url: 基础 URL，所有请求会基于此 URL
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.host = base_url.rstrip("/")  #self.host
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.session()  #创建一个会话实例，之后可以用这个实例来发送请求

        self.port = ''
        self.version = version
        self.env = env
        self.is_ssl = is_ssl


        # 设置默认请求头
        self.session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type':'application/json'
            }
        )


    def set_header(self,key:str,value:str)->None:
        """设置请求头"""
        self.session.headers[key] = value

    def set_headers(self, headers: Dict[str, str]) -> None:
        """批量设置请求头"""
        self.session.headers.update(headers)

    def set_auth(self, auth: tuple) -> None:
        """设置认证信息"""
        self.session.auth = auth

    def set_timeout(self, timeout: int) -> None:
        """设置超时时间"""
        self.timeout = timeout

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
        if self.port and len(self.port) > 0:
            print("1")
            return "%s://%s:%s%s" % (ssl_method, self.host, self.port, self.get_uri(url=url, version=version))
        else:
            print("2")
            return "%s://%s%s" % (ssl_method, self.host, self.get_uri(url=url, version=version))


    def _request(self,method:str,endpoint:str, params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Optional[requests.Response]:
        """
       执行 HTTP 请求

       Args:
           method: HTTP 方法 (GET, POST, PUT, DELETE, etc.)
           endpoint: 接口端点
           params: URL 参数
           data: 请求体数据
           json_data: JSON 格式的请求体数据
           headers: 请求头
           **kwargs: 其他传递给 requests 的参数

       Returns:
           Response 对象或 None (如果所有重试都失败)
       """
        # url = f"{self.host}/{endpoint.lstrip("/")}" if self.host else endpoint
        # url = f"{self.host}{self.version}/{endpoint.lstrip("/")}"
        url = self.get_url(endpoint.lstrip("/"),self.version)
        print(f"url = {url}")
        # 合并类级别和请求级别的 headers
        request_headers = {**self.session.headers, **(headers or {})}
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=self.timeout,
                    **kwargs
                )

                # 记录请求信息
                logger.info(f"{method} {url} - Status: {response.status_code}")

                # 如果请求成功，返回响应
                if response.status_code < 400:
                    return response

                # 如果是服务器错误，尝试重试
                if 500 <= response.status_code < 600 and attempt < self.max_retries - 1:
                    logger.warning(
                        f"Server error {response.status_code}, retrying... ({attempt + 1}/{self.max_retries})")
                    sleep(1)  # 等待一秒后重试
                    continue
                # 如果是客户端错误，不重试
                return response

            except Timeout:
                logger.warning(f"Request timeout, retrying... ({attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    sleep(1)  # 等待一秒后重试
                continue

            except RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    sleep(1)  # 等待一秒后重试
                continue

        logger.error(f"All {self.max_retries} attempts failed for {method} {url}")
        return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """发送 GET 请求"""
        # endpoint = self.version+endpoint
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(
            self,
            endpoint: str,
            data: Optional[Union[Dict[str, Any], str]] = None,  #表示这个参数可以是括号内的类型，也可以是None。所以data可以是指定的类型，也可以不传（即默认为None）。
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Optional[requests.Response]:
        """发送 POST 请求"""
        return self._request('POST', endpoint, data=data, json_data=json_data, **kwargs)

    def put(
            self,
            endpoint: str,
            data: Optional[Union[Dict[str, Any], str]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Optional[requests.Response]:
        """发送 PUT 请求"""
        return self._request('PUT', endpoint, data=data, json_data=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """发送 DELETE 请求"""
        return self._request('DELETE', endpoint, **kwargs)

    def patch(
            self,
            endpoint: str,
            data: Optional[Union[Dict[str, Any], str]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Optional[requests.Response]:
        """发送 PATCH 请求"""
        return self._request('PATCH', endpoint, data=data, json_data=json_data, **kwargs)

    def get_json(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[Any]:
        """发送 GET 请求并返回 JSON 数据"""
        response = self.get(endpoint, params=params, **kwargs)
        return self._parse_json_response(response) if response else None

    def post_json(
            self,
            endpoint: str,
            data: Optional[Union[Dict[str, Any], str]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Optional[Any]:
        """发送 POST 请求并返回 JSON 数据"""
        response = self.post(endpoint, data=data, json_data=json_data, **kwargs)
        return self._parse_json_response(response) if response else None

    @staticmethod
    def _parse_json_response(response: requests.Response) -> Optional[Any]:
        """解析 JSON 响应"""
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response.text}")
            return None

    def close(self):
        """关闭会话"""
        self.session.close()


if __name__ == "__main__":
    #创建 HTTP 客户端实例
    # base_url = 'mv-generate.sdp.101.com'
    # client = BaseHttp(base_url, version="v1.0")
    base_url ='llm-music.sdp.101.com'
    client = BaseHttp(base_url)

    try:
        #发送GET请求

        # params = {
        #     "resource_id" : "7c185a6e-a0e5-47b8-bcd2-6f8d05c8a75d"
        # }
        # response = client.get("/visitor/resource/info",params)
        # if response and response.status_code == 200:
        #     response_data = response.json()
        #     print("GET Response:", json.dumps(response_data, indent=4, ensure_ascii=False))
        #


        #发送POST请求
        body={
            "music_id":"3ad90474-2a06-4585-aa77-a987c6cc501f"
        }
        response = client.post(endpoint="/beats_info",json_data=body)
        if response and response.status_code == 200:
            response_data = response.json()
            print("POST Response:", json.dumps(response_data, indent=4, ensure_ascii=False))

    finally:
        # 关闭客户端
        client.close()