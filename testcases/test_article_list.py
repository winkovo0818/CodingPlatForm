# 读取系统配置
import allure
import pytest

from api.article_api import ArticleAPI
from api.user_api import UserAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from conftest import login_token
from utils.data_driver import load_test_data

config = read_yaml("data/config.yaml")
# 获取base_url
base_url = config["base_url"]


@allure.feature("文章模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/article_data.yaml", "article_cases"))
def test_article_list_param(title, request_data, validators, login_token):
    with allure.step(f"执行用例：{title}"):
        # login_token fixture现在会确保提供有效token

        article_api = ArticleAPI(base_url, login_token)
        # 调用获取文章列表API
        res = article_api.get_article_list(request_data)
        # 精简日志打印格式
        print_api_debug(title, res)
        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)
        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
