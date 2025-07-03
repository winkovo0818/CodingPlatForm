import requests
import logging


class RequestHandler:
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}

    def request(self, method, path, **kwargs):
        headers = kwargs.pop("headers", {})
        merged_headers = {**self.default_headers, **headers}
        url = self.base_url + path
        return requests.request(method=method, url=url, headers=merged_headers, **kwargs)
