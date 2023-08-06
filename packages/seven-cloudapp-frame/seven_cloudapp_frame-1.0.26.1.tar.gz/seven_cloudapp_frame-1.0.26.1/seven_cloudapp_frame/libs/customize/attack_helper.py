# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-22 13:32:07
@LastEditTime: 2022-06-15 13:36:30
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
import re

class AttackHelper:
    """
    :description:攻击帮助类
    """

    #sql关键字
    _sql_pattern_key = r"\b(and|like|exec|execute|insert|create|select|drop|grant|alter|delete|update|asc|count|chr|mid|limit|union|substring|declare|master|truncate|char|delclare|or)\b|(\*|;)"
    #Url攻击正则
    _url_attack_key = r"\b(alert|xp_cmdshell|xp_|sp_|restore|backup|administrators|localgroup)\b"

    @classmethod
    def is_contain_sql(self, str):
        """
        :description: 是否包含sql关键字
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        result = re.search(self._sql_pattern_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_routine_key(self, key):
        """
        :description: 过滤常规字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        routine_key_list = ["\u200b"]
        if not isinstance(key, str):
            return key
        for item in routine_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def filter_sql(self, key):
        """
        :description: 过滤sql关键字
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        result = re.findall(self._sql_pattern_key, key.lower())
        for item in result:
            key = key.replace(item[0], "")
            key = key.replace(item[0].upper(), "")
        return key

    @classmethod
    def filter_special_key(self, key):
        """
        :description: 过滤sql特殊字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def is_attack(self, str):
        """
        :description: 是否攻击请求
        :param str:当前请求地址
        :return:True是 False否
        :last_editors: HuangJianYi
        """
        if ":" in str:
            return True
        result = re.search(self._url_attack_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def check_attack_request(self):
        """
        :description: 校验是否攻击请求和是否包含非法参数值
        :return:True满足条件直接拦截 False不拦截
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        is_filter_attack = config.get_value("is_filter_attack", False)
        if is_filter_attack == True and self.request_params:
            for key in self.request_params.keys():
                if self.is_contain_sql(self.request_params[key]) or self.is_attack(self.request_params[key]):
                    invoke_result_data.success = False
                    invoke_result_data.error_code="attack_error"
                    invoke_result_data.error_message = f"参数{key}:值不合法"
                    break
        return invoke_result_data

    @classmethod
    def check_params(self, must_params):
        """
        :description: 校验必传参数
        :return:InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        must_array = []
        if type(must_params) == str:
            must_array = must_params.split(",")
        if type(must_params) == list:
            must_array = must_params
        for must_param in must_array:
            if not must_param in self.request_params or self.request_params[must_param] == "":
                invoke_result_data.success = False
                invoke_result_data.error_code="param_error"
                invoke_result_data.error_message = f"参数错误,缺少必传参数{must_param}"
                break
        return invoke_result_data