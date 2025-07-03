import os
import json
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import allure
from allure_commons.types import AttachmentType

class ReportHelper:
    """
    测试报告辅助工具类，用于提取测试结果数据、生成测试趋势图，
    并将测试趋势图添加到Allure报告中
    """

    @staticmethod
    def extract_test_results(allure_results_dir):
        """
        从Allure报告数据中提取测试结果统计信息

        Args:
            allure_results_dir: Allure报告数据目录

        Returns:
            dict: 包含测试结果统计信息的字典
        """
        # 初始化统计数据
        stats = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'broken': 0,
            'duration': 0
        }

        # 遍历Allure报告数据目录中的所有JSON文件
        for filename in os.listdir(allure_results_dir):
            if filename.endswith('-result.json'):
                file_path = os.path.join(allure_results_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        stats['total'] += 1

                        # 统计测试状态
                        status = data.get('status', '')
                        if status == 'passed':
                            stats['passed'] += 1
                        elif status == 'failed':
                            stats['failed'] += 1
                        elif status == 'skipped':
                            stats['skipped'] += 1
                        elif status == 'broken':
                            stats['broken'] += 1

                        # 累计测试时间
                        if 'stop' in data and 'start' in data:
                            stats['duration'] += data['stop'] - data['start']
                    except json.JSONDecodeError:
                        continue

        # 计算通过率
        if stats['total'] > 0:
            stats['pass_rate'] = round(stats['passed'] / stats['total'] * 100, 2)
        else:
            stats['pass_rate'] = 0

        # 转换持续时间为秒
        stats['duration'] = round(stats['duration'] / 1000, 2)

        # 添加时间戳
        stats['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stats['date'] = datetime.datetime.now().strftime('%Y-%m-%d')

        return stats

    @staticmethod
    def save_test_results(stats, csv_file):
        """
        将测试结果统计信息保存到CSV文件中

        Args:
            stats: 测试结果统计信息
            csv_file: CSV文件路径
        """
        # 检查CSV文件是否存在
        file_exists = os.path.isfile(csv_file)

        # 确保目录存在
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        # 写入CSV文件
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'date', 'total', 'passed', 'failed',
                         'skipped', 'broken', 'pass_rate', 'duration']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # 如果文件不存在，写入表头
            if not file_exists:
                writer.writeheader()

            # 写入数据
            writer.writerow({k: stats[k] for k in fieldnames})

    @staticmethod
    def generate_trend_charts(csv_file, output_dir):
        """
        从CSV文件中读取历史测试结果数据，生成测试趋势图

        Args:
            csv_file: CSV文件路径
            output_dir: 输出目录

        Returns:
            list: 生成的图表文件路径列表
        """
        # 检查CSV文件是否存在
        if not os.path.isfile(csv_file):
            return []

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 读取CSV文件
        df = pd.read_csv(csv_file)

        # 如果数据少于2条，无法生成趋势图
        if len(df) < 2:
            return []

        # 生成的图表文件路径列表
        chart_files = []

        # 设置图表样式
        plt.style.use('ggplot')

        # 1. 通过率趋势图
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['pass_rate'], marker='o', linestyle='-', color='green')
        plt.title('测试通过率趋势图')
        plt.xlabel('日期')
        plt.ylabel('通过率 (%)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 保存图表
        pass_rate_chart = os.path.join(output_dir, 'pass_rate_trend.png')
        plt.savefig(pass_rate_chart)
        plt.close()
        chart_files.append(pass_rate_chart)

        # 2. 测试用例数量趋势图
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['total'], marker='o', linestyle='-', label='总数')
        plt.plot(df['date'], df['passed'], marker='o', linestyle='-', label='通过')
        plt.plot(df['date'], df['failed'], marker='o', linestyle='-', label='失败')
        plt.plot(df['date'], df['skipped'], marker='o', linestyle='-', label='跳过')
        plt.title('测试用例数量趋势图')
        plt.xlabel('日期')
        plt.ylabel('数量')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 保存图表
        case_count_chart = os.path.join(output_dir, 'case_count_trend.png')
        plt.savefig(case_count_chart)
        plt.close()
        chart_files.append(case_count_chart)

        # 3. 测试执行时间趋势图
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['duration'], marker='o', linestyle='-', color='blue')
        plt.title('测试执行时间趋势图')
        plt.xlabel('日期')
        plt.ylabel('执行时间 (秒)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 保存图表
        duration_chart = os.path.join(output_dir, 'duration_trend.png')
        plt.savefig(duration_chart)
        plt.close()
        chart_files.append(duration_chart)

        return chart_files

    @staticmethod
    def attach_trend_charts_to_report(chart_files):
        """
        将测试趋势图添加到Allure报告中

        Args:
            chart_files: 图表文件路径列表
        """
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                with open(chart_file, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=os.path.basename(chart_file).replace('_trend.png', '').replace('_', ' ').title(),
                        attachment_type=AttachmentType.PNG
                    )

    @staticmethod
    def generate_test_summary(stats):
        """
        生成测试摘要信息

        Args:
            stats: 测试结果统计信息

        Returns:
            str: 测试摘要信息
        """
        summary = f"""
# 测试执行摘要

## 基本信息
- **执行时间**: {stats['timestamp']}
- **总执行时间**: {stats['duration']} 秒

## 测试结果统计
- **总用例数**: {stats['total']}
- **通过用例数**: {stats['passed']}
- **失败用例数**: {stats['failed']}
- **跳过用例数**: {stats['skipped']}
- **异常用例数**: {stats['broken']}
- **通过率**: {stats['pass_rate']}%
"""
        return summary

    @staticmethod
    def attach_test_summary(stats):
        """
        将测试摘要信息添加到Allure报告中

        Args:
            stats: 测试结果统计信息
        """
        summary = ReportHelper.generate_test_summary(stats)
        allure.attach(
            summary,
            name="测试执行摘要",
            attachment_type=AttachmentType.MARKDOWN
        )
