#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Tuner
@contact:chenjianpeng97@outlook.com
@version: 1.0.0
@license: Apache Licence
@file: main.py
@time: 2024/12/23 19:48
"""
import csv
from gherkin.parser import parse


def gherkin_to_zentao(gherkin_text):
    # 解析Gherkin文本
    feature = parse(gherkin_text)
    zentao_cases = []

    for feature_case in feature['feature']['children']:
        if feature_case['type'] == 'Scenario':
            scenario_title = f"用例标题+\"{feature_case['name']}\""
            zentao_cases.append(generate_case_row(feature['feature']['name'], scenario_title, feature_case['steps']))
        elif feature_case['type'] == 'ScenarioOutline':
            scenario_title = f"用例标题+\"{feature_case['name']}\""
            for example in feature_case['examples']:
                for example_row in example['rows']:
                    zentao_cases.append(
                        generate_case_row(feature['feature']['name'], scenario_title, feature_case['steps'],
                                          example_row))

    return zentao_cases


def generate_case_row(feature_name, scenario_title, steps, example_row=None):
    # 基础的用例行
    row = {
        "gherkin": f"{feature_name}",
        "zentao": f"{scenario_title}"
    }

    pre_conditions = []
    steps_list = []

    for step in steps:
        step_text = step['text']
        if step['keyword'] == "Given":
            pre_conditions.append(f"前置条件+\"{step_text}\\n\"")
        elif step['keyword'] == "When":
            steps_list.append(f"步骤+\"1. {step_text}\\n\"")
        elif step['keyword'] == "Then":
            steps_list.append(f"步骤+\"3. 查看预期结果\\n\"，预期+\"{step_text}\"")

    # 你可以在此处处理其他关键字，如 And 和 Rule

    row["pre_conditions"] = ''.join(pre_conditions)
    row["steps"] = ''.join(steps_list)

    return row


def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["gherkin", "zentao", "pre_conditions", "steps"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":

    gherkin_example = """
    Feature: 登录
      Scenario: 输入正确的用户名和密码
        Given 打开登录页面
        And 输入用户名和密码
        When 输入用户名和密码
        And 点击登录按钮
        Then 登录成功
        And 退出登录
    """

    zentao_cases = gherkin_to_zentao(gherkin_example)
    write_to_csv(zentao_cases, "zentao_cases.csv")
