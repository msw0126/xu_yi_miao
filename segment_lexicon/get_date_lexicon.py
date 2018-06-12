# -*- coding:utf-8 -*-
import datetime
import time

import os

import my_config


def get_date_list():
    date_list = []
    for x in range(1, 12000):
        year = str(datetime.date.today() + datetime.timedelta( days=int("-" + str(x) ) )).split("-")[0]
        month = str(datetime.date.today() + datetime.timedelta( days=int("-" + str(x) ) )).split("-")[1]
        day = str(datetime.date.today() + datetime.timedelta( days=int("-" + str(x) ) )).split("-")[2]
        if month.startswith("0"):
            month = month[1]
        if day.startswith("0"):
            day = day[1]
        date_list.append(year + "年" + month + "月" + day + "日")
        date_list.append( year + "_" + month + "_" + day)
        date_list.append( year + "." + month + "." + day )
        date_list.append(year + "年" + month + "月" )
        date_list.append(month + "月" + day + "日" )
    return date_list


if __name__ == '__main__':
    date_lexicon_path = os.path.join( my_config.data_path,"jieba_lexicon/date.txt")

    #得到日期的lisi
    date_list = get_date_list()
    #写入文件
    for date in date_list:
        with open( date_lexicon_path, 'a+', encoding='UTF-8' ) as f:
            f.write(date + "\n")