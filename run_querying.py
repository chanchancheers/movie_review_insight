from db_handler import DB
from make_wc import make_wc
from wordcloud import WordCloud
import time

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


    
make_wc(all_string, [], [], [], wordcloud)
time.sleep(10)