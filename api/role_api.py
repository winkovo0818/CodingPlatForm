from common.request_handler import RequestHandler


class RoleAPI:
    def __init__(self, base_url, token=None):
        default_headers = {"Authorization": f"{token}"} if token else {}
        self.client = RequestHandler(base_url, default_headers)

    # 获取角色列表
    def get_role_list(self, data):
        return self.client.request("post", "/role/list", json=data)

    # 获取角色详情
    def get_role_detail(self, role_id):
        return self.client.request("get", f"/role/detail/{role_id}")

    # 新增或修改角色
    def add_or_update_role(self, data):
        return self.client.request("post", "/role/save", json=data)
