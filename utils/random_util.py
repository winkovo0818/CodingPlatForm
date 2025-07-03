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
    def generate_email(domain="test.com"):
        """
        生成随机邮箱
        domain: 邮箱域名，默认为'test.com'
        """
        username = RandomUtil.generate_username(prefix="")
        return f"{username}@{domain}"

    @staticmethod
    def generate_phone():
        """
        生成随机手机号
        """
        # 手机号前三位列表
        prefix_list = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                      '150', '151', '152', '153', '155', '156', '157', '158', '159',
                      '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        # 随机选择前三位
        prefix = random.choice(prefix_list)
        # 生成后8位数字
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"
