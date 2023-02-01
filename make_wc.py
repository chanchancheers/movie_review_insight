import numpy as np
import pandas as pd
import os
import re
import seaborn as sns

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Hannanum, Mecab, Kkma
from PIL import Image

from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer

import time




def make_wc(txtfile, 
            names,
            not_expel, 
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
    
    new_nouns = nouns
    
    # for item in nouns:
    #     if len(item) != 1 or item in not_expel:
    #         new_nouns.append(item)

    # for item in excludings:
    #     if item in new_nouns:
    #         while item in new_nouns:
    #             new_nouns.remove(item)

    counter = Counter(new_nouns)         

    
    gen = wordcloud.generate_from_frequencies(counter)
    plt.figure(figsize=(20,20))
    plt.imshow(gen)
    wordcloud.to_file('./wordcloud_pics/picture.png')


