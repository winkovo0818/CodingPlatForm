import pytest
import allure
import copy
from api.user_api import UserAPI
from utils.data_driver import load_test_data
from common.yaml_util import read_yaml
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from utils.random_util import RandomUtil

config = read_yaml("data/config.yaml")
base_url = config["base_url"]


@allure.feature("用户注册模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/user_data.yaml", "register_cases"))
def test_register_param(title, request_data, validators):
    with allure.step(f"执行用例：{title}"):
        # 创建API实例
        user_api = UserAPI(base_url)

        # 深拷贝请求数据，避免修改原始数据
        modified_request_data = copy.deepcopy(request_data)

        # 如果是注册成功的用例，使用随机用户名
        if title == "注册成功":
            random_username = RandomUtil.generate_username()
            modified_request_data["username"] = random_username
            print(f"使用随机用户名: {random_username}")

        # 调用注册API
        res = user_api.register(modified_request_data)

        # 精简日志打印格式
        print_api_debug(title, res)

        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)

        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
