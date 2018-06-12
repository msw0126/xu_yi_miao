# -*- coding:utf-8 -*-
import os

import my_config


def read_file(filename):
    with open( filename, 'r', encoding='UTF-8') as f:
        L = []
        for _ in f:
            L.append( _.strip() )
        return L


def get_full_name_list(data):
    full_name_list = []
    for inx, i in enumerate( data ):
        full_name = i.split( "\t" )[1]
        if len( full_name ) < 1:
            continue
        full_name_list.append( full_name.replace( "-", "_" ).replace( "(", "_" ).replace( ")", "_" ) )
    return set(full_name_list)


def get_sec_name_list(data):
    sec_name_list = []
    for inx, i in enumerate( data ):
        sec_name = i.split( "\t" )[2]
        if len( sec_name ) < 2:
            continue
        sec_name_list.append( sec_name.replace( "-", "_" ).replace( "(", "_" ).replace( ")", "_" ) )
    return set(sec_name_list)


def save_file(content, file_path):
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content + "\n" )


def file_name(file_dir):
    l = []
    g = os.walk( file_dir )
    for path, d, filelist in g:
        for filename in filelist:
            if filename.endswith( 'txt' ):
                # print( os.path.join( path, filename ) )
                l.append( os.path.join( path, filename ) )
    return l


if __name__ == '__main__':
    lable_path = os.path.join( my_config.data_path,"lable_data/zengjianchi.train")
    share_lexicon_path = os.path.join( my_config.data_path,"jieba_lexicon/shareholder.txt")

    name_list = []
    data = read_file(lable_path)
    #股东全称
    full_name_list = get_full_name_list(data)
    for x in full_name_list:
        name_list.append(x)
    #股东简称
    sec_name_list = get_sec_name_list(data)
    for x in sec_name_list:
        name_list.append(x)

    #企业名称
    company_name_path = os.path.join( my_config.data_path,"jieba_lexicon/company_name.txt")
    company_name_data = read_file( company_name_path )
    for x in company_name_data:
        name_list.append(x)

    #去重复
    name_list_set = set(name_list)
    for name in name_list_set:
        save_file(name, share_lexicon_path)

    # # 删除在lable数据中没有id的训练数据txt文件
    # id_list = []
    # data = read_file( lable_path )
    # for inx, i in enumerate( data ):
    #     notice_id = i.split( "\t" )[0]
    #     id_list.append( notice_id )
    # sentence_txt_dir = "../data/train_data/train_sentence_txt/zeng_jian_chi/"
    # txt_file = file_name( sentence_txt_dir )
    # for file_path in txt_file:
    #     file_name = file_path.split( "/" )[-1].split( "." )[0]
    #     if file_name not in id_list:
    #         os.remove( file_path )







