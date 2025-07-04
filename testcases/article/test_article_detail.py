import allure
import pytest

from api.article_api import ArticleAPI
from common.debug_printer import print_api_debug
from common.test_helper import TestHelper
from common.yaml_util import read_yaml
from conftest import login_token
from utils.data_driver import load_test_data

# 读取系统配置
config = read_yaml("data/config.yaml")
# 获取base_url
base_url = config["base_url"]


@allure.feature("文章详情模块")
@pytest.mark.parametrize("title, request_data, validators",
                         load_test_data("data/article_data.yaml", "article_detail_cases"))
def test_article_detail_param(title, request_data, validators, login_token):
    with allure.step(f"执行用例：{title}"):
        # 创建带有token的API实例
        article_api = ArticleAPI(base_url, login_token)
        # 调用获取文章详情API
        res = article_api.get_article_detail(request_data["id"])
        # 精简日志打印格式
        print_api_debug(title, res)
        # 使用TestHelper附加测试信息到Allure报告
        TestHelper.attach_test_info(title, res)
        # 使用TestHelper验证响应
        TestHelper.validate_response(title, res, validators)
