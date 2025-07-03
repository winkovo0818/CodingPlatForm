import os
os.system("pytest testcases/ --alluredir=reports")
os.system("allure generate reports -o reports/html --clean")
os.system("allure open reports/html")
