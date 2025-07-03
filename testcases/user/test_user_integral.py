import pytest
import allure
from api.user_api import UserAPI
from utils.data_driver import load_test_data
from common.yaml_util import read_yaml
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper

config = read_yaml("data/config.yaml")
base_url = config["base_url"]


@allure.feature("用户积分模块")
@pytest.mark.parametrize("title, validators",
                         [(case["title"], case["validators"]) for case in read_yaml("data/user_data.yaml")["user_integral_cases"]])
def test_user_integral(title, validators, login_token):
    with allure.step(f"执行用例：{title}"):
        # 根据测试用例标题决定是否使用token
        # 如果是"用户未登录"的测试用例，则不使用token模拟未登录状态
        if "用户未登录" in title:
            # 创建不带token的API实例
            user_api = UserAPI(base_url)
        else:
            # 创建带token的API实例
            user_api = UserAPI(base_url, login_token)

        # 调用获取用户积分的API
        res = user_api.get_user_integral()

        # 精简日志打印格式
        print_api_debug(title, res)

        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)

        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
