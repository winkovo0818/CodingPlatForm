import time

import requests


class RequestHandler:
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}

    def request(self, method, path, **kwargs):
        headers = kwargs.pop("headers", {})
        merged_headers = {**self.default_headers, **headers}
        url = self.base_url + path
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 发送请求
        response = requests.request(method=method, url=url, headers=merged_headers, **kwargs)
        
        # 计算响应时间（毫秒）
        response_time = (time.time() - start_time) * 1000
        
        # 将响应时间添加到响应对象中
        response.elapsed_ms = response_time
        
        return response
