# -*- coding: utf-8 -*-
"""
@author: Lily
@contact: 你的邮箱
@created: 2025/9/24
AI hub 的鉴权信息
"""
default_time_out = 20000
appId = "b4fb92a0-af7f-49c2-b270-8f62afac1133"

class AIhubAuth:
    service_url ={
        "ol":"https://ai-hub-server.sdpsg.101.com/"
    }

    def __init__(self, user_id='336915', password = 'momocll343', env="ol"):
        super().__init__()
        self.userId = user_id
        self.pwd = password

        self.uc_service_url = AIhubAuth.service_url[env]

    @classmethod
    def get_headers(cls, method, url, header=None):
        auth = AIhubAuth.get_auth(method.upper(), url)
        headers = {
            "Userid":userId
            'X-App-Id': BOT_ID,
            'sdp-app-id': appId,
            'Content-Type': 'application/json',
            'Authorization': auth}
        if header is not None:
            headers.update(header)
        print(f"headers:/n {headers}")
        return headers