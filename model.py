#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Tuner
@contact:chenjianpeng97@outlook.com
@version: 1.0.0
@license: Apache Licence
@file: model.py
@time: 2025/1/1 12:35
"""
# define testcase model
from dataclasses import dataclass


@dataclass
class ZentaoTestcase:
    # 用例名称
    name: str
    # 前置条件
    precondition: str
    # 测试步骤
    step: str
    # 预期结果
    expected_result: str
    # 关键词
    keyword: str
    # 优先级
    priority: str
    # 用例类型
    case_type: str
    # 适用阶段
    apply_phase: str

if __name__ == '__main__':
    pass
