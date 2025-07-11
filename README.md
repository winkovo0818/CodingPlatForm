# API自动化测试框架

## 项目简介

这是一个基于Python的API自动化测试框架，用于测试RESTful API。框架采用了Page Object设计模式，将API调用封装在独立的类中，使测试用例更加清晰和易于维护。框架支持数据驱动测试，可以从YAML文件中加载测试数据，实现测试数据与测试逻辑的分离。

## 项目结构

```
auto-test-frame/
├── api/                  # API封装层
│   ├── article_api.py    # 文章相关API
│   └── user_api.py       # 用户相关API
├── common/               # 通用工具类
│   ├── assertions.py     # 断言工具
│   ├── debug_printer.py  # 调试打印工具
│   ├── request_handler.py # HTTP请求处理
│   ├── test_helper.py    # 测试辅助工具
│   └── yaml_util.py      # YAML文件读取
├── data/                 # 测试数据
│   ├── article_data.yaml # 文章测试数据
│   ├── config.yaml       # 配置数据
│   └── user_data.yaml    # 用户测试数据
├── testcases/            # 测试用例
│   ├── article/          # 文章相关测试
│   └── user/             # 用户相关测试
├── utils/                # 工具类
│   ├── data_driver.py    # 数据驱动测试
│   └── random_util.py    # 随机数据生成
├── conftest.py           # pytest配置
├── requirements.txt      # 项目依赖
└── run_tests.py          # 测试运行脚本
```

## 安装说明

### 前提条件

- Python 3.7+
- pip
- Allure (用于生成测试报告)

### 安装步骤

1. 克隆仓库
```bash
git clone <repository-url>
cd auto-test-frame
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 安装Allure
   - Windows: 使用Scoop安装
   ```bash
   scoop install allure
   ```
   - MacOS: 使用Homebrew安装
   ```bash
   brew install allure
   ```
   - Linux: 使用apt安装
   ```bash
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```

## 使用方法

### 配置

在`data/config.yaml`中配置测试环境信息：

```yaml
base_url: https://api.example.com
timeout: 30
```

### 运行测试

使用提供的脚本运行所有测试并生成Allure报告：
```bash
python run_tests.py
```

这将执行以下操作：
1. 运行所有测试用例并生成Allure报告数据
2. 从报告数据生成HTML报告
3. 自动打开HTML报告

如果要手动运行特定测试，可以使用以下命令：

```bash
# 运行特定模块的测试
pytest testcases/user/ --alluredir=reports

# 运行特定测试用例
pytest testcases/user/test_user_login.py --alluredir=reports

# 生成并查看报告
allure generate reports -o reports/html --clean
allure open reports/html
```

## 框架特性

### API封装

API调用被封装在独立的类中，例如：

```python
# api/user_api.py
class UserAPI:
    def login(self, username, password):
        # 实现登录API调用
        pass
```

### 数据驱动测试

从YAML文件加载测试数据：

```python
# testcases/user/test_user_login.py
@pytest.mark.parametrize("title, request_data, validators", load_test_data("user_data.yaml", "login"))
def test_user_login(title, request_data, validators):
    # 使用测试数据执行测试
    pass
```

### 断言工具

提供了丰富的断言方法：

```python
# 断言相等
Assert.equal(actual, expected, "Values should be equal")

# 断言包含
Assert.contains(text, substring, "Text should contain substring")

# 断言JSON键存在
Assert.json_key_exist(json_obj, key, "JSON should contain key")
```

### 测试辅助工具

提供了测试辅助方法：

```python
# 验证API响应
TestHelper.validate_response(response, validators)

# 附加测试信息到Allure报告
TestHelper.attach_test_info(title, content)
```

### 随机数据生成

提供了随机数据生成方法：

```python
# 生成随机用户名
username = RandomUtil.generate_username()

# 生成随机邮箱
email = RandomUtil.generate_email()

# 生成随机手机号
phone = RandomUtil.generate_phone()
```

## 示例

### 测试数据示例

```yaml
# data/user_data.yaml
login:
  - title: "登录成功"
    request:
      username: "testuser"
      password: "password123"
    validators:
      - eq: [status_code, 200]
      - contains: [message, "登录成功"]
      - json_key_exist: [data, token]
```

### 测试用例示例

```python
# testcases/user/test_user_login.py
import pytest
from api.user_api import UserAPI
from utils.data_driver import load_test_data

@pytest.mark.parametrize("title, request_data, validators", load_test_data("user_data.yaml", "login"))
def test_user_login(title, request_data, validators):
    # 创建API实例
    user_api = UserAPI()
    
    # 调用API
    response = user_api.login(request_data["username"], request_data["password"])
    
    # 验证响应
    from common.test_helper import TestHelper
    TestHelper.validate_response(response, validators)
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request
