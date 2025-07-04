# 读取系统配置
import copy

import allure
import pytest

from api.role_api import RoleAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from conftest import login_token
from utils.data_driver import load_test_data
from utils.random_util import RandomUtil

config = read_yaml("data/config.yaml")
# 获取base_url
base_url = config["base_url"]


@allure.feature("角色模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/role_data.yaml", "role_add_cases"))
def test_article_list_param(title, request_data, validators, login_token):
    with allure.step(f"执行用例：{title}"):
        # 创建API实例
        role_api = RoleAPI(base_url, login_token)

        # 深拷贝请求数据，避免修改原始数据
        modified_request_data = copy.deepcopy(request_data)

        # 如果是注册成功的用例，使用随机用户名
        if title == "添加角色成功":
            random_username = RandomUtil.generate_username()
            modified_request_data["roleName"] = random_username
            modified_request_data["roleKey"] = random_username

        res = role_api.add_or_update_role(modified_request_data)

        # 精简日志打印格式
        print_api_debug(title, res)

        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)

        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
