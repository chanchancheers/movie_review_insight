import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Crawling_thread(threading.Thread):
    def __init__(self, name, url, db_handler):
        super().__init__()
        self.name = f"Thread {name}"
        self.thread_num = name
        self.url = url
        self.driver = webdriver.Chrome('chromedriver')
        self.db_handler = db_handler

        self.__review_page_num = 100

    @property
    def deal_page_num(self):
        return self.__review_page_num
    @deal_page_num.setter
    def deal_page_num(self, number):
        self.__review_page_num = number
    @deal_page_num.deleter
    def deal_page_num(self):
        del self.__review_page_num


    def run(self):

        # movie_id 는 Thread 번호
        movie_id = int(self.thread_num)

        self.driver.get(self.url)
        try:
            movie_info_Se = self.driver.find_element(By.CLASS_NAME, 'mv_info')
        except:
            self.driver.close()
            return None

        title = movie_info_Se.find_element(By.TAG_NAME, 'a').get_attribute('text')
        title_n_year = movie_info_Se.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div[1]/strong').text
        title_eng = title_n_year[:-6]
        year = title_n_year[-4:]
        info_spec_Se = self.driver.find_element(By.CLASS_NAME,'info_spec')
        
        #아래로는 없을 수도 있음
        director_found = False
        try:
            director = info_spec_Se.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[2]/p/a').text
            director_found = True
        except:
            director = "NOT FOUND"
        
        score_found = False
        try:
            score_Se = movie_info_Se.find_element(By.CLASS_NAME, 'main_score')
            # star_score_Se = main_score_Se.find_elements(By.TAG_NAME, 'em')
            score_found = True

        
        except Exception as e:
            pass
        
        #줄거리 가져오기
        explanation = ""
        if score_found :
            try:
                explanation_Se = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[4]/div[1]/div/div[1]/p')
                explanation = explanation_Se.text
            except:
                pass

        if score_found :
            main_score_Se = movie_info_Se.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div[1]/div[1]')
            star_score_Se = main_score_Se.find_elements(By.TAG_NAME, 'em')
            
            #스코어들 모임
            scores = []
            score = []

            for i in star_score_Se:
                try:
                    #스코어 하나        
                    num = int(i.text)
                    score.append(num)
                    
                except :
                    pass
                if len(score) == 3 :
                        score_num = str(score[0]) + '.' + str(score[1]) + str(score[2])
                        scores.append(float(score_num))
                        score.clear()
            
            if scores:
                rating = round(sum(scores) / len(scores),2)
                # print("==", i.text, " ")

        time.sleep(0.5)

        print(f"{self.name} : {title}, {title_eng}, {year}")

        if not director_found:
            director = None
        if not score_found:
            rating = 0
        
        self.db_handler.insert_info(movie_id, title, title_eng, director, year, rating, explanation)
        self.db_handler.commit()




        #리뷰 크롤링
        
        if score_found:
            review_tab = self.driver.find_element(By.XPATH, '//*[@id="movieEndTabMenu"]/li[5]/a/em')
            review_tab.click()
            time.sleep(10)
            try:
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="pointAfterListIframe"]'))
            except Exception as e:
                return None

            #리뷰 n * 10 개로 제한(페이지 n개)
            # self.__review_page_num = 100

            next_onoff = True
            next_number = 2     # 다음 페이지 = 2부터 시작
            print(f"\n\nTHREAD {self.name} reviews collected.\n")
            while next_onoff and next_number <= self.__review_page_num:
                try:
                    score_result_Se = self.driver.find_element(By.XPATH, '/html/body/div/div/div[5]')
            
                except Exception as e:
                    pass
                
                try:
                    each_review_Se = score_result_Se.find_elements(By.TAG_NAME, 'li')
                except Exception as e:
                    pass

                for i, a_review in enumerate(each_review_Se):
                    try:
        
                        review_rating = a_review.find_element(By.TAG_NAME, 'em').text
                        #onclick이라는 항목이 있으면 눌러야됨...
                        content_Se = a_review.find_element(By.ID,f'_filtered_ment_{i}')

                        try:
                            content = content_Se.find_element(By.TAG_NAME, 'a').get_attribute('data-src')
                        except:
                            content = content_Se.text

                        
                        
                        self.db_handler.insert_review(movie_id, int(review_rating), content)
                        self.db_handler.commit()

                    except :
                        pass
                
                try:
                    next = self.driver.find_element(By.XPATH, f'//*[@id="pagerTagAnchor{next_number}"]/em')
                    if next.text == '다음':
                        next.click()
                        next_number += 1
                        time.sleep(0.1)
                    else :
                        next_onoff = False
                except:
                    next_onoff = False
        
        
            






class Crawler():
    def __init__(self, db, movie_name, review_page_num):
        self.db = db        
        self.__maximum_threads = 5
        self.movie_name = movie_name
        self.review_page_num = review_page_num

    @property
    def deal_maximum_threads(self):
        return self.__maximum_threads
    @deal_maximum_threads.setter
    def deal_maximum_threads(self, number):
        self.__maximum_threads = number
    @deal_maximum_threads.deleter
    def deal_maximum_threads(self):
        del self.__maximum_threads


    def crawling(self):
        
        #1. 페이지 입성
        driver = webdriver.Chrome('chromedriver')
        
        # 일단 아바타 하나로
        movies = self.movie_name
        main_page = rf'https://movie.naver.com/movie/search/result.naver?section=movie&query={movies}'
        driver.get(main_page)

        movie_urls = []

        next_onoff = True
        while next_onoff:
            search_1_Se = driver.find_element(By.XPATH, '//*[@id="old_content"]/ul[2]')
            result_thumb_Ses = search_1_Se.find_elements(By.CLASS_NAME, 'result_thumb')

            for target in result_thumb_Ses:
                a_Se = target.find_element(By.TAG_NAME, 'a')
                url = a_Se.get_attribute('href')
                movie_urls.append(url)
            try:
                to_next = driver.find_element(By.XPATH, '//*[@id="old_content"]/div[2]/table/tbody/tr/td[3]/a')
                if to_next.text == '다음':
                    to_next.click()
                    time.sleep(2)
                else:
                    next_onoff = False
                    time.sleep(2)
            except : 
                next_onoff = False

        
               
        
        #다음 페이지로 입장
        threads = []
        

        for i, target_url in enumerate(movie_urls, 1):
            thread = Crawling_thread(i, target_url, self.db)
            thread.deal_page_num = self.review_page_num
            thread.start()
            threads.append(thread)
            if i %  self.__maximum_threads == 0:
                for item in threads:
                    item.join()
                threads.clear()
        



            

        pass
    