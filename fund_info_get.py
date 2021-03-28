import re
import fund_daily_get
import datetime
import baostock as bs


def get_fund_name():
    """
    根据接口文本获得基金名字
    :return: 基金名字
    """
    # 获得接口文本
    content = fund_daily_get.get_content()
    # 正则表达式
    pattern = r'/\*基金或股票信息\*/var fS_name = "(.*)";var fS_code'
    # 查找结果
    search = re.findall(pattern, content)

    # 得到月净值涨跌幅
    fund_name = ''
    for i in search:
        fund_name = i
    return fund_name


def today_get():
    """
    获取今天时间并判断是不是22点前后
    :return: 今天这个时间点的交易日
    """

    # 获取当前时间
    clock = datetime.datetime.today()

    # 今天的日期
    d_end = datetime.date.today()
    # 向前推进一周
    if clock.hour < 22:
        day_change = datetime.timedelta(days=1)
    else:
        day_change = datetime.timedelta(days=0)
    d_end = d_end - day_change

    return d_end


def week_get(d_end):
    """
    获得一周前的日期
    :return: 一周前的日期
    """

    # 向前推进一周
    days_count = datetime.timedelta(days=7)
    d_start = d_end - days_count

    return d_start


def day_week():
    """
    获取一周内的交易天数
    :return: 一周内的交易天数
    """

    # 判断到最近一个交易日
    d_end = today_get()
    while 1:
        rs = bs.query_trade_dates(start_date=d_end, end_date=d_end)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        if data_list[0][1] == '1':
            break
        else:
            day_change = datetime.timedelta(days=1)
            d_end = d_end - day_change

    # 获取今天和一周前日期
    d_start = week_get(d_end)

    # 获取交易日信息
    rs = bs.query_trade_dates(start_date=d_start, end_date=d_end)
    # print('query_trade_dates respond error_code:' + rs.error_code)
    # print('query_trade_dates respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    # 获取一会走交易日数
    i = 0
    number_trade_day = 0
    for data in data_list:
        if data_list[i][1] == '1':
            number_trade_day += 1
        i += 1
    # 判断一周前是不是交易日
    if data_list[0][1] == '0':
        number_trade_day += 1

    return number_trade_day


def calculate_week_change(d):
    """
    通过fund_daily_get的列表计算周净值涨跌幅
    :return: 周净值涨跌幅
    """
    # 获得本基金每日净值
    NAV_list = fund_daily_get.fund_NAV()
    # 获取分红和拆分列表
    dividends, splits, dividends_value, splits_value = fund_daily_get.fund_dividends_and_splits()

    #  处理超出字符的情况
    dividends.append(999999998)
    splits.append(999999999)

    # 记录分红拆分日期日数
    dividends_number = 0
    splits_number = 0

    week_change = "(" + str(NAV_list[0])
    while 1:
        if dividends[dividends_number] < splits[splits_number]:
            if d - 1 < dividends[dividends_number]:
                week_change = week_change + "/" + str(NAV_list[d - 1]) + ") - 1"
                break
            else:
                week_change = week_change + "/(" + str(NAV_list[dividends[dividends_number] + 1]) + "-" + \
                              str(dividends_value[dividends_number]) + ")) * (" + \
                              str(NAV_list[dividends[dividends_number] + 1])
                dividends_number += 1
        else:
            if d - 1 < splits[splits_number]:
                week_change = week_change + "/" + str(NAV_list[d - 1]) + ") - 1"
                break
            else:
                week_change = week_change + "/(" + str(NAV_list[splits[splits_number] + 1]) + "/" + \
                              str(splits_value[splits_number]) + ")) * (" + \
                              str(NAV_list[splits[splits_number] + 1])
                splits_number += 1

    # 计算周涨跌幅
    week_change = round(eval(week_change) * 100, 2)

    return week_change


def get_month_change():
    """
    根据接口文本获得一月的涨跌幅
    :return: 一月的涨跌幅
    """
    # 获得接口文本
    content = fund_daily_get.get_content()
    # 正则表达式
    pattern = r'/\*近一月收益率\*/var syl_1y="(.*)";/\*股票仓位测算图\*/'
    # 查找结果
    search = re.findall(pattern, content)

    # 得到月净值涨跌幅
    month_change = 0
    for i in search:
        if i == '':
            month_change = '--'
        else:
            month_change = float(i)
    return month_change


def get_month3_change():
    """
    根据接口文本获得三月的涨跌幅
    :return: 三月的涨跌幅
    """
    # 获得接口文本
    content = fund_daily_get.get_content()
    # 正则表达式
    pattern = r'/\*近三月收益率\*/var syl_3y="(.*)";/\*近一月收益率\*/'
    # 查找结果
    search = re.findall(pattern, content)

    # 得到三月净值涨跌幅
    month3_change = 0
    for i in search:
        if i == '':
            month3_change = '--'
        else:
            month3_change = float(i)
    return month3_change


def get_month6_change():
    """
    根据接口文本获得六月的涨跌幅
    :return: 六月的涨跌幅
    """
    # 获得接口文本
    content = fund_daily_get.get_content()
    # 正则表达式
    pattern = r'/\*近6月收益率\*/var syl_6y="(.*)";/\*近三月收益率\*/'
    # 查找结果
    search = re.findall(pattern, content)

    # 得到六月净值涨跌幅
    month6_change = 0
    for i in search:
        if i == '':
            month6_change = '--'
        else:
            month6_change = float(i)
    return month6_change


def get_year_change():
    """
    根据接口文本获得一年的涨跌幅
    :return: 一年的涨跌幅
    """
    # 获得接口文本
    content = fund_daily_get.get_content()
    # 正则表达式
    pattern = r'/\*近一年收益率\*/var syl_1n="(.*)";/\*近6月收益率\*/'
    # 查找结果
    search = re.findall(pattern, content)

    # 得到一年净值涨跌幅
    year_change = 0
    for i in search:
        if i == '':
            year_change = '--'
        else:
            year_change = float(i)
    return year_change


def year3_get(d_end):
    """
    获得三年前的日期
    :return: 三年前的日期
    """

    d_start = d_end
    # 向前推进三年
    d_start = d_start.replace(year=d_start.year - 3)
    # 判断闰年前三年（29号改28号）
    if d_end.month == 2 and d_end.day == 29:
        d_start = d_start.replace(day=d_start.day - 1)

    return d_start


def day_year3():
    """
    获取三年内的交易天数
    :return: 三年内的交易天数
    """

    # 判断到最近一个交易日
    d_end = today_get()
    while 1:
        rs = bs.query_trade_dates(start_date=d_end, end_date=d_end)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        if data_list[0][1] == '1':
            break
        else:
            day_change = datetime.timedelta(days=1)
            d_end = d_end - day_change

    # 获取今天和一周前日期
    d_start = year3_get(d_end)

    # 获取交易日信息
    rs = bs.query_trade_dates(start_date=d_start, end_date=d_end)
    # print('query_trade_dates respond error_code:' + rs.error_code)
    # print('query_trade_dates respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    # 获取一会走交易日数
    i = 0
    number_trade_day = 0
    for data in data_list:
        if data_list[i][1] == '1':
            number_trade_day += 1
        i += 1
    # 判断一周前是不是交易日
    if data_list[0][1] == '0':
        number_trade_day += 1

    # 消除baostock交易日计算错误
    number_trade_day += 3

    return number_trade_day


def calculate_year3_change(d):
    """
    通过fund_daily_get的列表计算周净值涨跌幅
    :return: 周净值涨跌幅
    """
    # 获得本基金每日净值
    NAV_list = fund_daily_get.fund_NAV()
    # 获取分红和拆分列表
    dividends, splits, dividends_value, splits_value = fund_daily_get.fund_dividends_and_splits()

    #  处理超出字符的情况
    dividends.append(999999998)
    splits.append(999999999)

    # 记录分红拆分日期日数
    dividends_number = 0
    splits_number = 0

    week_change = "(" + str(NAV_list[0])
    while 1:
        if dividends[dividends_number] < splits[splits_number]:
            if d - 1 < dividends[dividends_number]:
                week_change = week_change + "/" + str(NAV_list[d - 1]) + ") - 1"
                break
            else:
                week_change = week_change + "/(" + str(NAV_list[dividends[dividends_number] + 1]) + "-" + \
                              str(dividends_value[dividends_number]) + ")) * (" + \
                              str(NAV_list[dividends[dividends_number] + 1])
                dividends_number += 1
        else:
            if d - 1 < splits[splits_number]:
                week_change = week_change + "/" + str(NAV_list[d - 1]) + ") - 1"
                break
            else:
                week_change = week_change + "/(" + str(NAV_list[splits[splits_number] + 1]) + "/" + \
                              str(splits_value[splits_number]) + ")) * (" + \
                              str(NAV_list[splits[splits_number] + 1])
                splits_number += 1

    # 计算周涨跌幅
    week_change = round(eval(week_change) * 100, 2)

    return week_change


def login():
    # 登陆系统
    bs.login()


def get_all(code, d_week, d_year3):
    fund_daily_get.set_code(code)
    number = len(fund_daily_get.fund_NAV())
    name = get_fund_name()
    w1 = '--'
    if number > 5:
        w1 = calculate_week_change(d_week)
    m1 = get_month_change()
    m3 = get_month3_change()
    m6 = get_month6_change()
    y1 = get_year_change()
    y3 = '--'
    if number >= d_year3:
        y3 = calculate_year3_change(d_year3)

    return name, w1, m1, m3, m6, y1, y3


# if __name__ == '__main__':
#     login()
#     code = "002190"
#     name, w1, m1, m3, m6, y1, y3 = get_all(code)
#
#     print("基金代码：{}，基金名字：{}，一周净值涨跌幅：{}，一月净值涨跌幅：{}，三月净值涨跌幅：{}，六月净值涨跌幅：{}，一年净值涨跌幅：{},"
#           "三年年净值涨跌幅：{}".format(code, name, w1, m1, m3, m6, y1, y3))
    # # print("基金代码：{}，基金名字：{}，三月净值涨跌幅：{}，三月净值涨跌幅：{}，".format(code, get_fund_name(), get_month3_change(), calculate_year3_change()))
    # calculate_year3_change()
