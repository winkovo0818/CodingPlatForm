import allure
from common.assertions import Assert


class TestHelper:
    @staticmethod
    def attach_test_info(title, res):
        """
        将测试信息附加到Allure报告中
        """
        allure.dynamic.title(title)
        allure.attach(str(res.request.url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
        if hasattr(res.request, 'body') and res.request.body:
            allure.attach(str(res.request.body), name="请求体", attachment_type=allure.attachment_type.TEXT)
        allure.attach(res.text, name="响应数据", attachment_type=allure.attachment_type.TEXT)

    @staticmethod
    def validate_response(title, res, validators):
        """
        验证API响应
        """
        print(f"响应内容: {res.text}")

        try:
            response_json = res.json()
            print(f"响应JSON: {response_json}")

            # 遍历validators中的所有断言
            for validator in validators:
                for key, expected_value in validator.items():
                    # 处理嵌套字段，如data.username
                    if isinstance(expected_value, dict) and key in response_json:
                        nested_obj = response_json[key]
                        for nested_key, nested_value in expected_value.items():
                            actual_nested_value = nested_obj.get(nested_key)
                            print(f"验证 {key}.{nested_key}: 实际值={actual_nested_value}, 期望值={nested_value}")
                            Assert.equal(actual_nested_value, nested_value, f"{title} - {key}.{nested_key}断言失败")
                    else:
                        actual_value = response_json.get(key)
                        print(f"验证 {key}: 实际值={actual_value}, 期望值={expected_value}")
                        Assert.equal(actual_value, expected_value, f"{title} - {key}断言失败")

        except Exception as e:
            print(f"解析响应JSON失败: {e}")
            raise
