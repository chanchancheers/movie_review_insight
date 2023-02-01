from db_handler import DB
from wordcloud import WordCloud
import streamlit as st
import time

import numpy as np
import pandas as pd
import os
import re
import seaborn as sns

import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Hannanum, Mecab, Kkma
from PIL import Image

from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer




def make_wc(txtfile, 
            # names,
            # not_expel, 
            excludings,
           wordcloud):
    processor = Mecab()
    strings = ''
    pattern = r"[^ㄱ-ㅎㅏ-ㅣa-zA-Z가-힣0-9 ]"
    regex = re.compile(pattern)
    
    
    # for item in names:
    #     strings = re.sub(item,'',strings)
        
    
    strings = txtfile
    nouns = processor.nouns(strings)
    
    new_nouns = []
    
    for item in nouns:
        if len(item) != 1 :
        # or item in not_expel:
            new_nouns.append(item)

    for item in excludings:
        if item in new_nouns:
            while item in new_nouns:
                new_nouns.remove(item)

    counter = Counter(new_nouns)         

    
    gen = wordcloud.generate_from_frequencies(counter)
    plt.figure(figsize=(20,20))
    plt.imshow(gen)
    wordcloud.to_file('./wordcloud_pics/picture.png')
    return gen





db = DB()


# searching_word = input("=== NOTE : 검색할 단어를 입력하세요. 단어를 포함한 리뷰를 불러옵니다. ===")



searching_word = '13'
query = f'''
        SELECT * FROM Reviews
        WHERE (POSITION('{searching_word}' in content) > 0);
'''

db.execute(query)
contents = db.fetchall()

all_string = ""
for content in contents:
    all_string += (content[1][1:-1] + ' ')

wordcloud = WordCloud(
                font_path = '/Library/Fonts/AppleSDGothicNeo.ttc', 
                          width=1000, height=1000, scale=2.0, 
                          max_font_size=250, colormap = 'tab20b', 
                          max_words = 200, background_color='white')


excludings = [
    '아바타','제임스','카메론','그동안', '감독', '최근', '이게', '이걸', '과정', '그때', '그것', '요즘', '리마'
    ,'영화','작품','텐데','때문','하나','이건','정도','하나', '당시', '레이', '동안', '개봉', '러닝', '타임'

]
make_wc(all_string, excludings, wordcloud)

img = Image.open('./wordcloud_pics/picture.png')


st.write(f"\"{searching_word}\" 문자열을 포함하는 리뷰들의 워드클라우드")
st.image(img)
