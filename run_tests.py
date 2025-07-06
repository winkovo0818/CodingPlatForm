# import os
# os.system("pytest testcases/ --alluredir=reports")
import os
import subprocess
import sys

# 创建reports目录（如果不存在）
if not os.path.exists("reports"):
    os.makedirs("reports")

if not os.path.exists("reports/coverage"):
    os.makedirs("reports/coverage")

# 运行测试，同时收集覆盖率数据和Allure报告数据
print("运行测试并收集覆盖率数据...")
result = subprocess.run([
    "pytest",
    "testcases/",
    "--alluredir=reports",  # 生成Allure报告数据
    "--cov=api",  # 只收集API模块的覆盖率
    "--cov-report=html:reports/coverage",
    "--cov-report=term"
], check=False)

# 尝试生成Allure报告
os.system("allure generate reports -o reports/html --clean")
os.system("allure open reports/html")

print("\n覆盖率报告已生成到 reports/coverage 目录")
print("请在浏览器中打开 reports/coverage/index.html 查看详细的覆盖率报告")

# 返回pytest的退出码
sys.exit(result.returncode)
