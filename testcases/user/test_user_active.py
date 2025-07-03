import allure
import pytest

from api.user_api import UserAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from utils.data_driver import load_test_data

config = read_yaml("data/config.yaml")
base_url = config["base_url"]


@allure.feature("用户活跃度模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/user_data.yaml", "user_activity_cases"))
def test_user_statistics_param(title, request_data, validators):
    user_api = UserAPI(base_url)
    res = user_api.user_active_ranking()
    # 精简日志打印格式
    print_api_debug(title, res)

    # 使用TestHelper附加测试信息到Allure报告
    TestHelper.attach_test_info(title, res)

    # 使用TestHelper验证响应
    TestHelper.validate_response(title, res, validators)
