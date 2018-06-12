# -*- coding:utf-8 -*-

import os

import my_config
import pandas as pd


def read_file(file_path):
    return open(file_path, encoding='utf-8').read()


if __name__ == '__main__':
    html_path = os.path.join(my_config.data_path, "train_data/train_html/zeng_jian_chi/107140.html")
    html_data = read_file(html_path)
    print( pd.read_html( html_data, header=0, encoding='utf8' ))
    print("--------------------------------")
    print(pd.read_html(html_data, header=0, encoding='utf8')[0]['股东名称'].values)