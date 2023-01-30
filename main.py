from db_handler import DB
from crawler import Crawler

db = DB('movie_info')
db.execute_only_once()

print("DB reinitialized")

crawler = Crawler(db)

crawler.crawling()