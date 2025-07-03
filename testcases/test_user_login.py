import pytest
import allure
from api.user_api import UserAPI
from utils.data_driver import load_test_data
from common.yaml_util import read_yaml
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper

config = read_yaml("data/config.yaml")
base_url = config["base_url"]
user_api = UserAPI(base_url)


@allure.feature("用户登录模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/user_data.yaml", "login_cases"))
def test_login_param(title, request_data, validators):
    with allure.step(f"执行用例：{title}"):
        res = user_api.login(request_data)

        # 精简日志打印格式
        print_api_debug(title, res)

        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)
        
        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
