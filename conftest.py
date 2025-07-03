import time

import pytest

from api.user_api import UserAPI
from common.yaml_util import read_yaml


def get_token(base_url=None):
    """
    获取登录token的辅助函数，可以在fixture和测试中复用
    """
    if base_url is None:
        base_url = read_yaml("data/config.yaml")["base_url"]
    
    login_data = read_yaml("data/user_data.yaml")["login"]["valid"]
    api = UserAPI(base_url)
    
    try:
        res = api.login(login_data)
        response_json = res.json()
        print(f"登录响应: {response_json}")
        
        token = response_json.get("data", {}).get("token", "")
        if not token:
            print("警告: 登录成功但未获取到token")
        return token
    except Exception as e:
        print(f"登录获取token失败: {e}")
        return ""


@pytest.fixture(scope="session")
def login_token():
    """
    提供登录token的fixture，如果获取失败会重试
    """
    # 尝试获取token，增加重试次数和等待时间
    token = ""
    max_retries = 5  # 增加重试次数
    retry_count = 0
    
    while not token and retry_count < max_retries:
        if retry_count > 0:
            wait_time = retry_count * 2  # 递增等待时间
            print(f"重试获取token ({retry_count}/{max_retries})...等待{wait_time}秒")
            time.sleep(wait_time)  # 重试前等待更长时间
            
        token = get_token()
        retry_count += 1
    
    if not token:
        pytest.fail("无法获取有效的登录token，测试无法继续")  # 使测试失败而不是继续执行
    else:
        print(f"成功获取token: {token[:10]}...")
        
    return token
