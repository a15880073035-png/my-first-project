"""
http 请求分装

"""

import requests
from config import settings

class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json"
        }


    def request(self,method,choose_url,endpoint,params=None,data=None,json=None ):
        base_url =settings.current_config[choose_url]
        print( base_url)
        url = f"{base_url}{endpoint}"
        response = self.session.request(
            method =method,
            url= url,
            params = params,
            data = data,
            json = json,
            headers = self.headers
        )
        return response