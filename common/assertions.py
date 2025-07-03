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
