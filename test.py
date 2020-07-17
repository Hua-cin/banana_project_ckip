import json
import jieba
import os
import pandas as pd
import jieba.analyse
import datetime
from ckiptagger import WS, POS, NER
import re
import time
import pickle

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

def df_to_json():

    path = './01_ref_data/article_lib'
    file_list = os.listdir(path)

    columns = ["category", "title", "content"]
    news_total_data = []

    for i in file_list:

        c = i.split('_')[1].split('相關')[0]

        path_title = path + '/' + i
        file_title = os.listdir(path_title)

        for y in file_title:
            news_data = []
            t = y.split('_')[1].split('.')[0]
            new_content = path_title + '/' + y
            with open(new_content, 'r', encoding='utf-8') as f:
                a = f.read()

            news_data.append(c)
            news_data.append(t)
            news_data.append(a)
            news_total_data.append(news_data)

    new_df = pd.DataFrame(columns=columns)
    new_df = new_df.append(pd.DataFrame(news_total_data, columns=columns))

    new_df_json = new_df.to_json(orient="records", force_ascii=False)

    return (new_df_json)

def load_news_data():
    """
    新聞資料當作測試資料，產生訓練集向量與訓練集分類。
    :return: 訓練集的向量及訓練集分類
    """

    training_set_tf = {}
    training_set_class = {}
    keywords = []

    news_data = json.loads(df_to_json())

    for news in news_data:
        training_set_class[news['title']] = news['category']
        # 保存每篇文章詞彙出現次數
        # jieba.analyse.set_stop_words('./01_ref_data/stopword.txt')
        # seg_list = jieba.analyse.extract_tags(news['content'], topK=100)

        seg_list = ckip_sort_list(news['content'], topK=100)

        seg_content = {}
        for seg in seg_list:
            if seg in seg_content:
                seg_content[seg] += 1
            else:
                seg_content[seg] = 1
        # 保存文章詞彙頻率
        training_set_tf[news['title']] = seg_content
        # 獲取關鍵詞
        keywords.extend(jieba.analyse.extract_tags(news['content'], topK=100))
    # 文章斷詞轉成向量表示
    seg_corpus = list(set(keywords))
    for title in training_set_tf:
        tf_list = list()
        for word in seg_corpus:
            if word in training_set_tf[title]:
                tf_list.append(training_set_tf[title][word])
            else:
                tf_list.append(0)
        training_set_tf[title] = tf_list

    return (training_set_tf, training_set_class, seg_corpus)


ckip_training_set_tf, ckip_training_set_class, ckip_seg_corpus = load_news_data()



def func_out_file(name, content):

    resource_path = r'./print_file'
    if os.path.exists(resource_path) :  # 檢查目錄是否存在, 如已存在則強制刪除目錄並再次建立目錄
        time.sleep(0.1) # delay 秒, 避免目錄存取錯誤
    else :  # 目錄不存在, 則建立新目錄
        os.mkdir(resource_path)

    with open(r'{}/{}.txt'.format(resource_path, name), 'w', encoding='utf-8') as w:
        w.write(content)






print(ckip_training_set_tf)
print(ckip_training_set_class)
print(ckip_seg_corpus)


file = open('ckip_state', 'wb')
pickle.dump(ckip_training_set_tf, file)
pickle.dump(ckip_training_set_class, file)
pickle.dump(ckip_seg_corpus, file)
file.close()
