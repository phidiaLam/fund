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

    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text

    return content


def fund_daily():
    """
    根据网络接口数据，得到每日净值列表
    :param code: 基金代码
    :return: 返回从今到开售每日净值列表
    """
    # 获得接口文本
    content = get_content()

    # 正则表达式
    pattern1 = r'var Data_ACWorthTrend = \[(.*)\];/\*累计收益率走势\*/'
    # 查找结果
    search = re.findall(pattern1, content)

    # 储存基金每日净值
    daily_list = []

    # 获取每天净值走势
    for i in search:
        # [1459180800000,1.0] 获取所以的逗号后面的值
        pattern2 = r'(?<=,)\d\.\d+'
        data = re.findall(pattern2, i)
        for daily_value in data:
            daily = float(daily_value)
            daily_list.append(daily)
    print(len(daily_list))
    daily_list.reverse()
    return daily_list


def set_code(codes):
    """
    设置传入基金代码为全局变量
    :param codes: 传入基金代码
    """
    global code
    code = codes


if __name__ == '__main__':
    set_code("002190")
    # code = "002190"  # 基金代码
    print(fund_daily())
