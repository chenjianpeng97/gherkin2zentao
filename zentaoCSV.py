#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Tuner
@contact:chenjianpeng97@outlook.com
@version: 1.0.0
@license: Apache Licence
@file: zentaoCSV.py
@time: 2025/1/8 17:41
"""
from model import ZentaoTestcase


def gherkin2zentaoCSV(gherkin: dict) -> None:
    """
    :param gherkin:
    :return:
    """
    zentao_testcases = []

    # 提取feature标题，作为用例名通用前缀
    feature_name = gherkin['name']
    # 提取background部分，作为用例公共前置条件
    background = gherkin['background']
    # 提取不在Rule下的Scenario，作为用例
    scenarios = gherkin['scenarios']
    # 提取不在Rule下的Scenario_outline，作为用例
    scenario_outlines = gherkin['scenario_outline']
    # 提取Rule，作为用例分组
    rules = gherkin['rules']
    # 储存CSV列信息
    testcase_name_list = []
    preconditions_list = []
    steps_list = []
    # 1. 生成不再Rule下的Scenario用例
    for scenario in scenarios:
        # 1.1 生成用例名
        testcase_name = f"【{feature_name}】+{scenario['name']}"
        testcase_name_list.append(testcase_name)
        # 1.2 生成前置条件
        preconditions = background['steps'] if background else []
        preconditions_str = ''.join([str(index) + '. ' + step['keyword'] + ' '
                                     + step['name'] + '\n' for index, step in enumerate(preconditions, start=1)])
        preconditions_list.append(preconditions_str)
        # 1.3 生成步骤
        steps = scenario['steps']
        steps_str = ''.join(
            [str(index) + '. ' + step['keyword'] + ' ' + step['name'] + '\n' for index, step in
             enumerate(steps, start=1)])
        steps_list.append(steps_str)
    # 2. 生成不在Rule下的Scenario_outline用例
    for scenario_outline in scenario_outlines:
        step_index = 0
        # 2.1 生成用例名
        testcase_name = f"【{feature_name}】+{scenario_outline['name']}"
        testcase_name_list.append(testcase_name)
        # 2.2 生成前置条件
        preconditions = background['steps'] if background else []
        preconditions_str = ''.join([str(index) + '. ' + step['keyword'] + ' '
                                     + step['name'] + '\n' for index, step in enumerate(preconditions, start=1)])
        preconditions_list.append(preconditions_str)
        # 2.3 生成步骤
        steps = scenario_outline['steps']
        steps_str = ''.join(
            [str(index) + '. ' + step['keyword'] + ' ' + step['name'] + '\n' for index, step in
             enumerate(steps, start=1)])
        # 步骤中测试数据集
        step_index = len(steps)
        examples = scenario_outline['examples']
        for example in examples:
            steps_str = ''.join(
                [str(index + step_index) + '. ' + example['name'] + ' ' + '\n' for index, step in
                 enumerate(example, start=0)])
        steps_list.append(steps_str)

        # 拼接到CSV中
        row = {"用例名称": testcase_name_list, "前置条件": preconditions_list, "步骤": steps_list}


if __name__ == '__main__':
    testdict = {'name': '功能名解析测试', 'description': [],
                'background': {'name': '背景信息解析测试', 'steps': [
                    {'keyword': 'Given', 'name': '背景步骤1', 'text': None, 'table': None},
                    {'keyword': 'And', 'name': '背景步骤2', 'text': None, 'table': None}]},
                'scenarios': [
                    {'name': '常规场景解析测试',
                     'steps': [{'keyword': 'Given', 'name': '常规场景解析测试步骤1', 'text': None,
                                'table': None},
                               {'keyword': 'And', 'name': '常规场景解析测试步骤2', 'text': None,
                                'table': None},
                               {'keyword': 'When', 'name': '常规场景解析测试步骤3', 'text': None,
                                'table': None},
                               {'keyword': 'And', 'name': '常规场景解析测试步骤4', 'text': None,
                                'table': None},
                               {'keyword': 'Then', 'name': '常规场景解析测试步骤5', 'text': None,
                                'table': None},
                               {'keyword': 'And', 'name': '常规场景解析测试步骤6', 'text': None,
                                'table': None}]},
                    {'name': '带doc string的场景解析测试', 'steps': [
                        {'keyword': 'Given', 'name': '带doc string的场景解析测试步骤1',
                         'text': 'doc string内容', 'table': None}]},
                    {'name': '带data table的场景解析测试', 'steps': [
                        {'keyword': 'Given', 'name': '带data table的场景解析测试步骤1', 'text': None,
                         'table': '列1,列2\n值1,值2'}]}, {'name': '带tags的场景解析测试', 'steps': [
                        {'keyword': 'Given', 'name': '带tags的场景解析测试步骤1', 'text': None,
                         'table': None},
                        {'keyword': 'When', 'name': '带tags的场景解析测试步骤2', 'text': None,
                         'table': None},
                        {'keyword': 'Then', 'name': '带tags的场景解析测试步骤3', 'text': None,
                         'table': None}]}],
                'scenario_outline': [{'name': 'Scenario Outline解析测试',
                                      'examples': [
                                          {'name': '测试数据集1', 'table': 'step1,step2,step3\n1,2,3'},
                                          {'name': '测试数据集2', 'table': 'step1,step2,step3\n4,5,6'}],
                                      'steps': [
                                          {'keyword': 'Given',
                                           'name': 'Scenario Outline解析测试<step1>', 'text': None,
                                           'table': None},
                                          {'keyword': 'When', 'name': 'Scenario Outline解析测试<step2>',
                                           'text': None,
                                           'table': None},
                                          {'keyword': 'Then', 'name': 'Scenario Outline解析测试<step3>',
                                           'text': None,
                                           'table': None}]}],
                'rules': [{'name': 'Rule解析测试', 'description': [],
                           'background': {'name': 'Rule解析测试背景',
                                          'steps': [{'keyword': 'Given',
                                                     'name': 'Rule解析测试背景步骤1',
                                                     'text': None,
                                                     'table': None},
                                                    {'keyword': 'And',
                                                     'name': 'Rule解析测试背景步骤2',
                                                     'text': None,
                                                     'table': None}]},
                           'scenarios': [{'name': 'Rule解析测试步骤1',
                                          'steps': [{'keyword': 'Given',
                                                     'name': 'Rule解析测试步骤1',
                                                     'text': None,
                                                     'table': None},
                                                    {'keyword': 'When',
                                                     'name': 'Rule解析测试步骤2',
                                                     'text': None,
                                                     'table': None},
                                                    {'keyword': 'Then',
                                                     'name': 'Rule解析测试步骤3',
                                                     'text': None,
                                                     'table': None}]}],
                           'scenario_outline': []}]}
    gherkin2zentaoCSV(testdict)
pass
