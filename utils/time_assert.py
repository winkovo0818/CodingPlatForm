#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
from typing import Union


class TimeAssert:
    """
    响应时间断言工具类
    
    提供了一系列方法来断言HTTP请求的响应时间是否在预期的区间范围内。
    """
    
    @staticmethod
    def assert_time_less_than(response, max_time: float):
        """
        断言响应时间小于指定的最大时间
        
        Args:
            response: HTTP响应对象，必须包含elapsed_ms属性
            max_time: 最大允许时间（毫秒）
            
        Raises:
            AssertionError: 如果响应时间大于或等于最大允许时间
        """
        elapsed_ms = getattr(response, 'elapsed_ms', None)
        if elapsed_ms is None:
            elapsed_ms = response.elapsed.total_seconds() * 1000
            
        with allure.step(f"断言响应时间小于 {max_time} 毫秒"):
            allure.attach(f"{elapsed_ms:.2f}", "实际响应时间(ms)", allure.attachment_type.TEXT)
            assert elapsed_ms < max_time, f"响应时间 {elapsed_ms:.2f}ms 超过了最大允许时间 {max_time}ms"
    
    @staticmethod
    def assert_time_greater_than(response, min_time: float):
        """
        断言响应时间大于指定的最小时间
        
        Args:
            response: HTTP响应对象，必须包含elapsed_ms属性
            min_time: 最小期望时间（毫秒）
            
        Raises:
            AssertionError: 如果响应时间小于或等于最小期望时间
        """
        elapsed_ms = getattr(response, 'elapsed_ms', None)
        if elapsed_ms is None:
            elapsed_ms = response.elapsed.total_seconds() * 1000
            
        with allure.step(f"断言响应时间大于 {min_time} 毫秒"):
            allure.attach(f"{elapsed_ms:.2f}", "实际响应时间(ms)", allure.attachment_type.TEXT)
            assert elapsed_ms > min_time, f"响应时间 {elapsed_ms:.2f}ms 小于最小期望时间 {min_time}ms"
    
    @staticmethod
    def assert_time_between(response, min_time: float, max_time: float):
        """
        断言响应时间在指定的区间范围内
        
        Args:
            response: HTTP响应对象，必须包含elapsed_ms属性
            min_time: 最小期望时间（毫秒）
            max_time: 最大允许时间（毫秒）
            
        Raises:
            AssertionError: 如果响应时间不在指定的区间范围内
            ValueError: 如果min_time大于或等于max_time
        """
        if min_time >= max_time:
            raise ValueError(f"最小期望时间 {min_time}ms 必须小于最大允许时间 {max_time}ms")
            
        elapsed_ms = getattr(response, 'elapsed_ms', None)
        if elapsed_ms is None:
            elapsed_ms = response.elapsed.total_seconds() * 1000
            
        with allure.step(f"断言响应时间在 {min_time} - {max_time} 毫秒之间"):
            allure.attach(f"{elapsed_ms:.2f}", "实际响应时间(ms)", allure.attachment_type.TEXT)
            assert min_time < elapsed_ms < max_time, f"响应时间 {elapsed_ms:.2f}ms 不在期望区间 {min_time}ms - {max_time}ms 内"
    
    @staticmethod
    def assert_time_approximately(response, expected_time: float, tolerance: Union[float, int, float]):
        """
        断言响应时间在预期时间的指定误差范围内
        
        Args:
            response: HTTP响应对象，必须包含elapsed_ms属性
            expected_time: 预期响应时间（毫秒）
            tolerance: 允许的误差范围，可以是具体的毫秒数或百分比（0.1表示10%）
            
        Raises:
            AssertionError: 如果响应时间不在预期时间的指定误差范围内
        """
        elapsed_ms = getattr(response, 'elapsed_ms', None)
        if elapsed_ms is None:
            elapsed_ms = response.elapsed.total_seconds() * 1000
            
        if isinstance(tolerance, float) and tolerance < 1:
            # 百分比误差
            min_time = expected_time * (1 - tolerance)
            max_time = expected_time * (1 + tolerance)
            tolerance_desc = f"{tolerance * 100}%"
        else:
            # 具体毫秒数误差
            min_time = expected_time - tolerance
            max_time = expected_time + tolerance
            tolerance_desc = f"{tolerance}ms"
            
        with allure.step(f"断言响应时间在预期时间 {expected_time}ms 的 {tolerance_desc} 误差范围内"):
            allure.attach(f"{elapsed_ms:.2f}", "实际响应时间(ms)", allure.attachment_type.TEXT)
            assert min_time <= elapsed_ms <= max_time, f"响应时间 {elapsed_ms:.2f}ms 不在预期时间 {expected_time}ms 的 {tolerance_desc} 误差范围内"
