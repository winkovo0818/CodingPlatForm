import random
import string
import time


class RandomUtil:
    @staticmethod
    def generate_username(prefix="test_user_"):
        """
        生成随机用户名
        prefix: 用户名前缀，默认为'test_user_'
        """
        # 生成6位随机字母和数字的组合
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # 添加时间戳后缀以确保唯一性
        timestamp = str(int(time.time()))[-4:]
        return f"{prefix}{random_str}_{timestamp}"

    @staticmethod
    # 随机生成角色名称
    def generate_role_name(prefix="test_role_"):
        """
        生成随机角色名称
        prefix: 角色名称前缀，默认为'test_role_'
        """
        # 生成6位随机字母和数字的组合
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # 添加时间戳后缀以确保唯一性
        timestamp = str(int(time.time()))[-4:]
        return f"{prefix}{random_str}_{timestamp}"

