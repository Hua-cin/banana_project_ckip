# -*- coding: utf-8 -*-
# from ckiptagger import data_utils
# data_utils.download_data_gdown("../")

# -*- coding: utf-8 -*-
from ckiptagger import WS, POS, NER
import os
import re
import jieba
import jieba.analyse
import datetime

#
# # insert stopword list
# stopword_path = r'./01_ref_data/stopword.txt'
# stopword_list = []
# with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
#     for temp in f_stop.readlines():
#         stopword_list.append(temp.replace('\n', ''))
#
# print(stopword_list)
#
#
# # insert source data
# path = r'./01_ref_data/content'
# file_list = os.listdir(path)
# text = ''
#
# for each_article in file_list:
#     # print(each_article)
#     article_path = path + "/" + each_article
#     with open(article_path, 'r', encoding = 'utf-8') as f:
#         temp = f.read()
#         for line in temp:
#             text += line.strip()
#
#
# # text = '傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。'
# ws = WS("../data")
# ws_results = ws([text])
#
# print(ws_results)
#
# ckip_word_count = {}
#
# for i in ws_results[0]:
#     if i in ckip_word_count:
#         ckip_word_count[i] += 1
#     else:
#         ckip_word_count[i] = 1
#
# print(ckip_word_count)
#
# ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if (len(k)>1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+',k)]
# ckip_word_list.sort(key=lambda item: item[1], reverse=True)
# print(ckip_word_list)
#
# l = []
# for i in ckip_word_list:
#     l.append(i[0])
#
# x = 10
# if len(l) >= x:
#     rl = l[0:x]
# else:
#     rl = l
#
# print(rl)

def ckip_sort_list(text, topK=100):
    '''
    text to sorted list
    '''

    text = text.replace('\n', ' ')

    # insert stopword list
    stopword_path = r'./01_ref_data/stopword.txt'
    stopword_list = []
    with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
        for temp in f_stop.readlines():
            stopword_list.append(temp.replace('\n', ''))

    ws = WS("../data")
    ws_results = ws([text])

    ckip_word_count = {}
    for i in ws_results[0]:
        if i in ckip_word_count:
            ckip_word_count[i] += 1
        else:
            ckip_word_count[i] = 1

    ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if
                      (len(k) > 1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+', k)]
    ckip_word_list.sort(key=lambda item: item[1], reverse=True)

    word_list = []
    for i in ckip_word_list:
        word_list.append(i[0])

    if len(word_list) >= topK:
        new_word_list = word_list[0:topK]
    else:
        new_word_list = word_list

    return new_word_list

# x = '''
# 余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
# 〔記者陳彥廷／屏東報導〕傳統的水果行整把香蕉50元左右，但買回家易過熟，現在小家庭居多，也無法即時吃完，最後丟棄浪費，南州蕉農余致榮搭上輕食風，將香蕉切把分開賣，除了外銷日本，連便利商店也相中好攜帶食用的切把香蕉，市場通路大開。
# 40歲出頭的余致榮，祖父輩就已開始種香蕉，從小看著香蕉長大，卻曾「討厭」香蕉，後來也當到紡織廠經理，但10年前母親生病，他回家接手，沒想到從此成為興趣，2年前他與通路商合作，將外銷日本的香蕉切把，約5條1小包，到日本就能直接上架，而多的1、2根香蕉則看準小家庭，直送國內的便利超商。
# 余致榮表示，從2月到6月生產的冬蕉品質最好，也是外銷黃金期，現在一星期外銷一貨櫃，還供量販超市、批發市場等，不但賣綠香蕉也幫客戶摧熟。
# 余致榮現在有近10公頃蕉田，他說，原本討厭香蕉，現在卻變成他的專業，向香蕉研究所請益後，運用施肥克服連做問題，更解決黃葉病，同一塊地竟能連種4年香蕉，也讓他獲得「施肥達人」頭銜。
# 余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根，他認為香蕉市場還有空間，現在他的洗選場成立，一年四季都能供應國內香蕉。
# 余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
# '''
#
# # insert source data
# path = r'./01_ref_data/content'
# file_list = os.listdir(path)
# text = ''
#
# for each_article in file_list:
#     # print(each_article)
#     article_path = path + "/" + each_article
#     with open(article_path, 'r', encoding = 'utf-8') as f:
#         temp = f.read()
#         for line in temp:
#             text += line.strip()
# x=text
#
# print("xxx")
# before_ckip = datetime.datetime.now()
# print(ckip_sort_list(x))
# after_ckip = datetime.datetime.now()
# print('spend {}'.format(after_ckip-before_ckip))
#
#
# before_jieba = datetime.datetime.now()
# jieba.analyse.set_stop_words('./01_ref_data/stopword.txt')
# seg_list = jieba.analyse.extract_tags(x, topK=100)
# print(seg_list)
# after_jieba = datetime.datetime.now()
# print('spend {}'.format(after_jieba-before_jieba))





def func_ckip(text):
    '''
    text to sorted list
    '''

    text = text.replace('\n', ' ')

    # insert stopword list
    stopword_path = r'./01_ref_data/stopword.txt'
    stopword_list = []
    with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
        for temp in f_stop.readlines():
            stopword_list.append(temp.replace('\n', ''))

    ws = WS("../data")
    ws_results = ws([text])

    ckip_word_count = {}
    for i in ws_results[0]:
        if i in ckip_word_count:
            ckip_word_count[i] += 1
        else:
            ckip_word_count[i] = 1

    ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if
                      (len(k) > 1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+', k)]
    ckip_word_list.sort(key=lambda item: item[1], reverse=True)

    ckip_dict = {}
    for i in ckip_word_list:
        ckip_dict[i[0]] =i [1]

    return ckip_dict







x = '''
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
〔記者陳彥廷／屏東報導〕傳統的水果行整把香蕉50元左右，但買回家易過熟，現在小家庭居多，也無法即時吃完，最後丟棄浪費，南州蕉農余致榮搭上輕食風，將香蕉切把分開賣，除了外銷日本，連便利商店也相中好攜帶食用的切把香蕉，市場通路大開。
40歲出頭的余致榮，祖父輩就已開始種香蕉，從小看著香蕉長大，卻曾「討厭」香蕉，後來也當到紡織廠經理，但10年前母親生病，他回家接手，沒想到從此成為興趣，2年前他與通路商合作，將外銷日本的香蕉切把，約5條1小包，到日本就能直接上架，而多的1、2根香蕉則看準小家庭，直送國內的便利超商。
余致榮表示，從2月到6月生產的冬蕉品質最好，也是外銷黃金期，現在一星期外銷一貨櫃，還供量販超市、批發市場等，不但賣綠香蕉也幫客戶摧熟。
余致榮現在有近10公頃蕉田，他說，原本討厭香蕉，現在卻變成他的專業，向香蕉研究所請益後，運用施肥克服連做問題，更解決黃葉病，同一塊地竟能連種4年香蕉，也讓他獲得「施肥達人」頭銜。
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根，他認為香蕉市場還有空間，現在他的洗選場成立，一年四季都能供應國內香蕉。
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
'''









before_ckip = datetime.datetime.now()
print(func_ckip(x))
after_ckip = datetime.datetime.now()
print('spend {}'.format(after_ckip-before_ckip))

before_ckip = datetime.datetime.now()
print(func_ckip(x))
after_ckip = datetime.datetime.now()
print('spend {}'.format(after_ckip-before_ckip))

before_ckip = datetime.datetime.now()
print(func_ckip(x))
after_ckip = datetime.datetime.now()
print('spend {}'.format(after_ckip-before_ckip))


