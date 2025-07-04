import allure
import pytest

from api.role_api import RoleAPI
from api.user_api import UserAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from utils.data_driver import load_test_data
from utils.random_util import RandomUtil

# 读取系统配置
config = read_yaml("data/config.yaml")
# 获取base_url
base_url = config["base_url"]


@allure.feature("角色模块")
@pytest.mark.parametrize("title, request_data, validators", load_test_data("data/user_data.yaml", "user_role_assignment_cases"))
def test_user_role_assignment(title, request_data, validators, login_token):
    user_api = UserAPI(base_url,login_token)
    role_api = RoleAPI(base_url, login_token)

    register_data = {
        "username": RandomUtil.generate_username(),
        "password": "admin",
        "confirmPassword": "admin",
        "nickname": RandomUtil.generate_username()
    }
    # 这里先创建一个用户
    resp = user_api.register(register_data).json()
    # 获取用户id
    user_id = resp["data"]

    # 创建一个角色 并获取角色id
    role_data = {
        "roleId": 0,
        "roleName": RandomUtil.generate_username(),
        "roleKey": RandomUtil.generate_username()
    }
    role_resp = role_api.add_or_update_role(role_data).json()

    role_id = role_resp["data"]

    # 给用户分配角色
    user_role_data = {
        "userId": user_id,
        "roleId": [role_id]
    }

    # 调用用户角色分配接口
    res = user_api.assign_role(user_role_data)
    # 精简日志打印格式
    print_api_debug(title, res)

    # 使用TestHelper附加测试信息到Allure报告
    TestHelper.attach_test_info(title, res)

    # 使用TestHelper验证响应
    TestHelper.validate_response(title, res, validators)


