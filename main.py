from db_handler import DB
from crawler import Crawler

db = DB('movie_info')
db.execute_only_once()

print("DB reinitialized")

#영화 제목으로 검색할 문자열
movie_name = '아바타'
#크롤링할 리뷰 페이지 갯수(기본설정 100)
review_page_num = 100
#동시에 돌릴 Thread의 갯수(기본설정 5)
maximum_threads_num = 5



crawler = Crawler(db, movie_name, review_page_num)

crawler.deal_maximum_threads(maximum_threads_num)


crawler.crawling()