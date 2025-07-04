class Assert:
    @staticmethod
    def equal(actual, expected, msg=""):
        if actual != expected:
            raise AssertionError(f"\n❌ 断言失败: {msg}\n👉 实际值: {actual}，期望值: {expected}")

    @staticmethod
    def contains(actual_text, expected_substring, msg=""):
        assert expected_substring in actual_text, msg or f"'{expected_substring}' not found in '{actual_text}'"

    @staticmethod
    def is_true(condition, msg=""):
        assert condition, msg or "情况不成立"

    @staticmethod
    def json_key_exist(json_data, key, msg=""):
        assert key in json_data, msg or f"Key '{key}' 在json数据中不存在"


class TimeAssert:
    """
    响应时间断言类，用于验证接口响应时间
    """

    def __init__(self):
        """
        初始化响应时间断言类
        """
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    @staticmethod
    def assert_less_than(actual_time, expected_time, msg=""):
        """
        静态方法：断言响应时间小于指定时间
        :param actual_time: 实际响应时间（毫秒）
        :param expected_time: 预期响应时间（毫秒）
        :param msg: 断言失败时的消息
        """
        if not (actual_time < expected_time):
            raise AssertionError(
                f"\n❌ 响应时间断言失败: {msg}\n👉 实际响应时间: {actual_time:.2f}ms，期望小于: {expected_time}ms")
