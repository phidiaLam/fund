"""
Autor: Wentao Lin
Description:
Date: 2021-01-22 12:19:31
LastEditTime: 2021-01-22 13:15:06
LastEditors: Wentao Lin
"""
import requests
import re
from fake_useragent import UserAgent
import time


def get_url():
    """
    根据基金代码生成爬取网页
    :param code: 基金代码
    :return: 爬取网页
    """
    url = "http://fund.eastmoney.com/pingzhongdata/%s.js" % code

    return url


def get_content():
    """
    根据基金代码和网址获得接口文本
    :param code: 基金代码
    :return: 接口文本
    """
    url = get_url()
    # 生成随机浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': UserAgent().random}
    while True:
        try:  # 外包一层try
            r = requests.get(url, headers=headers, timeout=500)
            # 返回信息
            content = r.text
            r.close()
            break
        except:
            time.sleep(5)
    return content


def fund_accumulative_total():
    """
    根据网络接口数据，得到每日累计净值列表
    :param code: 基金代码
    :return: 返回从今到开售每日累计净值列表
    """
    # 获得接口文本
    content = get_content()

    # 正则表达式
    pattern1 = r'var Data_ACWorthTrend = \[(.*)\];/\*累计收益率走势\*/'
    # 查找结果
    search = re.findall(pattern1, content)

    # 储存基金每日累计净值
    accumulative_total_list = []

    # 获取每天累计净值走势
    for i in search:
        # [1459180800000,1.0] 获取所以的逗号后面的值
        pattern2 = r'(?<=,)\d\.\d+'
        data = re.findall(pattern2, i)
        for daily_value in data:
            daily = float(daily_value)
            accumulative_total_list.append(daily)
    accumulative_total_list.reverse()
    print(len(accumulative_total_list))
    return accumulative_total_list


def fund_NAV():
    """
    根据网络接口数据，得到每日单位净值列表
    :return: 返回从今到开售每日单位净值列表
    """
    # 获得接口文本
    content = get_content()

    # 正则表达式
    pattern1 = r'"y":(\d+.\d+),"equityReturn"'
    # 查找结果
    search = re.findall(pattern1, content)
    # 储存基金每日单位净值
    NAV_list = []

    # 获取每天单位净值走势
    for i in search:
        daily = float(i)
        NAV_list.append(daily)
    NAV_list.reverse()
    return NAV_list


def fund_NAV_content():
    """
    根据网络接口数据，得到每日单位净值文本列表
    :return: 返回从今到开售每日单位净值文本列表
    """
    # 获得接口文本
    content = get_content()

    # 正则表达式
    pattern1 = r'var Data_netWorthTrend = \[(.*)\];\/\*累计净值走势\*\/'
    # 查找结果
    search = re.findall(pattern1, content)
    # print(search)
    # 储存基金每日单位净值
    search_list = []

    # 获取每天单位净值走势
    for i in search:
        # 正则表达式
        pattern1 = r'{([\w\"\":,.\-\"：\"]+)'
        # 查找结果
        search_list = re.findall(pattern1, i)
    search_list.reverse()
    return search_list


def fund_dividends_and_splits():
    """
    根据每日净值文本列表获取分红和拆分的日期
    :return: 分红日期列表和拆分日期列表
    """
    # 获取每日净值文本列表
    content = fund_NAV_content()

    # 储存分红和拆分的列表
    dividends = []
    splits = []
    dividends_value = []
    splits_value = []

    # 判断是否分红或拆分
    for index, value in enumerate(content):
        if "分红" in value:
            dividends.append(index)
            # 正则表达式
            pattern1 = r'现金(\d+\.\d+)元'
            # 查找结果
            search = re.findall(pattern1, value)
            for i in search:
                i = float(i)
                dividends_value.append(i)
        if "拆分" in value:
            splits.append(index)
            # 正则表达式
            pattern1 = r'折算(\d+\.\d+)份'
            # 查找结果
            search = re.findall(pattern1, value)
            for i in search:
                i = float(i)
                splits_value.append(i)

    return dividends, splits, dividends_value, splits_value


def set_code(codes):
    """
    设置传入基金代码为全局变量
    :param codes: 传入基金代码
    """
    global code
    code = codes


if __name__ == '__main__':
    set_code("161725")
    # code = "002190"  # 基金代码
    # a=25
    # b=27
    # print(fund_NAV()[a]-fund_NAV()[b])
    # print(fund_accumulative_total()[a]-fund_accumulative_total()[b])
    # print(fund_NAV())
    # print(fund_accumulative_total())
    dividends, splits, dividends_value, splits_value = fund_dividends_and_splits()
    print(dividends)
    print(splits)
    print(dividends_value)
    print(splits_value)
