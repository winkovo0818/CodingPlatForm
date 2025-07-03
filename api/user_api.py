from common.request_handler import RequestHandler


class UserAPI:
    def __init__(self, base_url, token=None):
        default_headers = {"Authorization": f"{token}"} if token else {}
        self.client = RequestHandler(base_url, default_headers)

    def login(self, data):
        return self.client.request("post", "/user/login", json=data)

    def register(self, data):
        return self.client.request("post", "/user/register", json=data)

    def logout(self):
        return self.client.request("get", "/user/logout")

    # 获取用户信息
    def get_user_info(self, userId):
        return self.client.request("get", f"/user/{userId}")

    # 获取用户统计信息
    def user_statistics(self, userId):
        return self.client.request("get", f"/user/statistics/{userId}")
    
    # 获取用户积分
    def get_user_integral(self):
        return self.client.request("get", "/user/integral")
