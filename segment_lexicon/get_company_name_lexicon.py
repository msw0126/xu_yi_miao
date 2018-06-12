# -*- coding:utf-8 -*-

import json

import os

import my_config


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        return f.readline()


def get_jieba_lexicon(json_file_path):
    jieba_lexicon = []
    company_name_list = json.loads( read_file( json_file_path ) )["data"]
    for name_dict in company_name_list:
        # print( "++++++++++++++++++++++++++++++++++++++++++++" )
        # print( name_dict )
        if "secShortName" in name_dict.keys():
            # print( name_dict["secShortName"] )
            jieba_lexicon.append( name_dict["secShortName"] )
        if "secFullName" in name_dict.keys():
            # print( name_dict["secFullName"] )
            jieba_lexicon.append( name_dict["secFullName"] )
        if "secShortNameChg" in name_dict.keys():
            secShortNameChg_list = name_dict["secShortNameChg"].split( "," )
            for name in secShortNameChg_list:
                # print( name )
                jieba_lexicon.append( name )
    return jieba_lexicon


if __name__ == '__main__':
    json_file_path = os.path.join( my_config.data_path,"FDDC_announcements_company_name_20180531.json")
    jieba_lexicon_path = os.path.join( my_config.data_path,"jieba_lexicon/company_name.txt")

    """解析json文件得到公司名称列表"""
    company_list = get_jieba_lexicon(json_file_path)
    """保存公司名称到分词字典文件"""

    for name in company_list:
        with open( jieba_lexicon_path, 'a+', encoding='UTF-8' ) as f:
            f.write(name + "\n")