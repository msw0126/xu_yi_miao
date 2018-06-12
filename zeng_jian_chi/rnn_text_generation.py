# -*- coding:utf-8 -*-
import os

import jieba
import multiprocessing
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from gensim.models.word2vec import Word2Vec

import my_config


def read_file(filename):
    """
    读文件，并把不利于分词的符号替换
    :param filename:
    :return:
    """
    with open(filename, 'r', encoding='UTF-8') as f:
        return f.read().strip()\
            .replace("（", "_")\
            .replace("）", "_")\
            .replace("/", "_")\
            .replace("(", "_")\
            .replace(")", "_")\
            .replace("-", "_")\
            .replace(",", "") \
            .replace( "】", "_" ) \
            .replace( "【", "_" )


def get_fenci(file_path):
    """
    分词
    :param file_path:
    :return:
    """
    seg_list = jieba.lcut(read_file(file_path))
    return seg_list


def file_name(file_dir, endswith_str="txt"):
    """
    得到参数目录下的所有文件
    :param file_dir:
    :return:
    """
    l = []
    g = os.walk( file_dir )
    for path, d, filelist in g:
        for filename in filelist:
            if filename.endswith( endswith_str ):
                # print( os.path.join( path, filename ) )
                l.append( os.path.join( path, filename ) )
    return l


def predict_next(input_array):
    x = np.reshape( input_array, (-1, seq_length, 128) )
    y = model.predict( x )
    return y


def string_to_index(raw_input):
    raw_input = raw_input.strip()
    input_stream = get_fenci( raw_input )
    res = []
    for word in input_stream[(len( input_stream ) - seq_length):]:
        res.append( w2v_model[word] )
    return res


def y_to_word(y):
    word_ = w2v_model.most_similar( positive=y, topn=1 )
    return word_


def generate_article(init, rounds=30):
    in_string = init.strip()
    for i in range(rounds):
        n = y_to_word(predict_next(string_to_index(in_string)))
        in_string += ' ' + n[0][0]
    return in_string


if __name__ == '__main__':
    # 加载分词字典
    company_lexicon = os.path.join( my_config.data_path, "jieba_lexicon/shareholder.txt" )
    date_lexicon = os.path.join( my_config.data_path, "jieba_lexicon/date.txt" )
    other_lexicon = os.path.join( my_config.data_path, "jieba_lexicon/other.txt" )
    jieba.load_userdict( company_lexicon )
    jieba.load_userdict( date_lexicon )
    jieba.load_userdict( other_lexicon )
    #得到所有需要分词的txt文件（不含表格的txt文件）
    without_table_path = os.path.join(my_config.data_path, "train_data/train_txt/zeng_jian_chi/without_table")
    corpus = []
    for file in file_name(without_table_path):
        word_list = get_fenci(file)
        corpus.append(word_list)
    print( len( corpus ) )
    print( corpus[:3] )
    #todo 词向量训练与lstm模型训练，有bug
    # w2v_model = Word2Vec( corpus, size=128, window=5, min_count=1, workers=multiprocessing.cpu_count() )
    # print(w2v_model['北京首都开发股份有限公司'])
    # raw_input = [item for sublist in corpus for item in sublist]
    # text_stream = []
    # vocab = w2v_model.vocab
    # for word_text in raw_input:
    #     print( "--------------------------" )
    #     print( vocab[100] )
    #     print(word_text)
    #     if word_text in vocab:
    #         text_stream.append( word_text )
    # print(len( text_stream ))
    #
    # #构建训练测试集
    # seq_length = 10
    # x = []
    # y = []
    # for i in range( 0, len( text_stream ) - seq_length ):
    #     given = text_stream[i:i + seq_length]
    #     predict = text_stream[i + seq_length]
    #     x.append( np.array( [w2v_model[word] for word in given] ) )
    #     y.append( w2v_model[predict] )
    # x = np.reshape( x, (-1, seq_length, 128) )
    # y = np.reshape( y, (-1, 128) )
    #
    # #模型构建
    # model = Sequential()
    # model.add( LSTM( 256, dropout_W=0.2, dropout_U=0.2, input_shape=(seq_length, 128) ) )
    # model.add( Dropout( 0.2 ) )
    # model.add( Dense( 128, activation='sigmoid' ) )
    # model.compile( loss='mse', optimizer='adam' )
    #
    # #跑模型
    # model.fit( x, y, nb_epoch=50, batch_size=4096 )
    #
    # #测试模型
    # init = '证券代码：000672证券简称：上峰水泥公告编号：2014-24'
    # article = generate_article( init )
    # print( '证券代码：000672证券简称：上峰水泥公告编号：2014-24', "===>", article)