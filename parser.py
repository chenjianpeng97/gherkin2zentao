#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Tuner
@contact:chenjianpeng97@outlook.com
@version: 1.0.0
@license: Apache Licence
@file: parser.py
@time: 2025/1/8 15:56
"""
import json
from behave.parser import parse_file


def table_to_string(table):
    if table is None:
        return None
    """
    将gherkin表格转换为字符串
    """
    headers = [header.strip() for header in table.headings]
    rows = [row.cells for row in table.rows]
    return '\n'.join([','.join(headers)] + [','.join(row) for row in rows])


# 解析 feature 文件
def parse_feature_file(filename):
    feature = parse_file(filename)
    print(f"Feature: {feature}")
    return feature


# 将 Feature 对象转换为字典
def feature_to_dict(feature) -> dict:
    """
    gherkin树型结构说明
    Feature has background, scenarios, scenario_outline, rules
    Rule has background, scenarios, scenario_outline
    Scenario has steps
    ScenarioOutline has steps, examples
    step has keyword, name, text, table
    输出dict格式feature
    """

    return {
        'name': feature.name,
        'description': feature.description,
        'background': {'name': feature.background.name,
                       'steps': [{'keyword': step.keyword, 'name': step.name, 'text': step.text,
                                  'table': table_to_string(step.table)}
                                 for step in feature.background.steps]},
        'scenarios': [
            {
                'name': scenario.name,
                'steps': [
                    {
                        'keyword': step.keyword,
                        'name': step.name,
                        'text': step.text,
                        'table': table_to_string(step.table)

                    } for step in scenario.steps
                ]
            } for scenario in feature.scenarios if scenario.type != 'scenario_outline'
        ],
        'scenario_outline': [
            {
                'name': scenario.name,
                'examples': [{'name': example.name, 'table': table_to_string(example.table)}
                             for example in scenario.examples],
                'steps': [
                    {
                        'keyword': step.keyword,
                        'name': step.name,
                        'text': step.text,
                        'table': table_to_string(step.table)
                    } for step in scenario.steps
                ]
            } for scenario in feature.scenarios if scenario.type == 'scenario_outline'
        ],
        'rules': [
            {'name': rule.name,
             'description': rule.description,
             'background': {'name': rule.background.name,
                            'steps': [
                                {'keyword': step.keyword, 'name': step.name, 'text': step.text,
                                 'table': table_to_string(step.table)}
                                for step in rule.background.steps]},
             'scenarios': [
                 {
                     'name': scenario.name,
                     'steps': [
                         {
                             'keyword': step.keyword,
                             'name': step.name,
                             'text': step.text,
                             'table': table_to_string(step.table)

                         } for step in scenario.steps
                     ]
                 } for scenario in rule.scenarios if scenario.type != 'scenario_outline'
             ],
             'scenario_outline': [
                 {
                     'name': scenario.name,
                     'examples': [{'name': example.name, 'table': example.table}
                                  for example in scenario.examples],
                     'steps': [
                         {
                             'keyword': step.keyword,
                             'name': step.name,
                             'text': step.text,
                             'table': table_to_string(step.table)
                         } for step in scenario.steps
                     ]
                 } for scenario in rule.scenarios if scenario.type == 'scenario_outline'
             ]} for rule in feature.rules
        ]
    }

    # 主函数


if __name__ == "__main__":
    feature_file = 'example.feature'  # 指定您的 feature 文件
    feature = parse_feature_file(feature_file)
    feature_dict = feature_to_dict(feature)

    # 转换为 JSON 格式并打印
    feature_json = json.dumps(feature_dict, indent=4)
    # 输出json到文件
    with open('example.json', 'w', encoding='utf-8') as f:
        f.write(feature_json)
    with open('example.json', 'r', encoding='utf-8') as f:
        loaded_json = json.load(f)
        print(loaded_json)
