# -*- coding:utf-8 -*-

import html2text
import re

import os
from lxml import html

import my_config
from bs4 import BeautifulSoup


def read_file_list(filename):
    with open( filename, 'r', encoding='UTF-8') as f:
        L = []
        for _ in f:
            L.append( _.strip() )
        return L


class ClassifyTableTxt(object):
    def __init__(self):
        self.md = html2text.HTML2Text()
        self.md.ignore_links = True
        self.md.ignore_images = True
        self.md.single_line_break = True
        self.md.wrap_links = False
        self.md.unicode_snob = True  # Prevents accents removing
        self.md.skip_internal_links = True
        self.md.ignore_anchors = True
        self.md.body_width = 0
        self.md.use_automatic_links = True

    def read_file(self, file_path):
        """
        读文件
        :param file_path:
        :return:
        """
        return open(file_path, encoding='utf-8').read()

    def save_file(self, file_path, content):
        """
        保存文件
        :param file_path:
        :param content:
        :return:
        """
        with open( file_path, 'a+', encoding='UTF-8' ) as f:
            f.write( content )

    def html_into_text(self, html_data):
        """
        HTML转txt,并保存为一行
        :param html_data:
        :return:
        """
        try:
            return self.md.handle( html_data ).replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' ).replace( ' ', '' )
        except:
            raise Exception

    # def html_into_text(self, html_data):
    #     """
    #     HTML转TXT文本
    #     :param html_data:
    #     :return:
    #     """
    #     return html2text.html2text( html_data )

    def classify_table_txt(self, html_path):
        """
        根据HTML文件中是否包含表格内容进行分类，并保存文件
        :param html_path:
        :return:
        """
        html_data = self.read_file(html_path)
        file_name = html_path.split("/")[-1].split(".")[0]
        if "<table" in html_data:
            # 将表格内容删除
            html_data = re.sub( '<table.*(?=>)(.|\n)*?</table>', '', html_data )
            self.save_file( os.path.join( my_config.data_path,
                                          "train_data/train_txt/zeng_jian_chi/contain_table/{}.txt".format( file_name)),
                       self.html_into_text( html_data ) )
        else:
            self.save_file(os.path.join(my_config.data_path,
                                        "train_data/train_txt/zeng_jian_chi/without_table/{}.txt".format(file_name)),
                      self.html_into_text(html_data))


if __name__ == '__main__':
    #先从lable数据中获取哪些html文件是已经有y的
    lable_data_path = os.path.join(my_config.data_path, "lable_data/zeng_jian_chi/zengjianchi.train")
    lable_data = read_file_list(lable_data_path)
    txt_list = set()
    for x in lable_data:
        txt_list.add(x.split("\t")[0])
    #对所有已经有标注数据的html文件进行转成txt操作
    for i in txt_list:
        html_path = os.path.join(my_config.data_path, "train_data/train_html/zeng_jian_chi/{}.html".format(i))
        c = ClassifyTableTxt()
        c.classify_table_txt(html_path)