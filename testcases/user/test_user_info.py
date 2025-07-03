import allure
import pytest

from api.user_api import UserAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from utils.data_driver import load_test_data

config = read_yaml("data/config.yaml")
base_url = config["base_url"]


@allure.feature("用户信息模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/user_data.yaml", "userInfo_cases"))
def test_user_info_param(title, request_data, validators, login_token):
    with allure.step(f"执行用例：{title}"):
        # 打印token信息，用于调试
        print(f"获取到的token: {login_token}")
        
        # login_token fixture现在会确保提供有效token
        
        # 创建带有token的API实例
        user_api = UserAPI(base_url, login_token)
        
        # 调用获取用户信息API
        res = user_api.get_user_info(request_data["id"])

        # 精简日志打印格式
        print_api_debug(title, res)

        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)
        
        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
