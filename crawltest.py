
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('chromedriver')

url = 'https://movie.naver.com/movie/bi/mi/point.naver?code=74977'

driver.get(url)

driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="pointAfterListIframe"]'))

next_onoff = True
next_number = 2

while next_onoff and next_number <= 15:
    try:
        score_result_Se = driver.find_element(By.XPATH, '/html/body/div/div/div[5]')

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
                print("\nFOUND\n")
            except:
                content = content_Se.text
                print("\nNOT FOUND\n")

            print(content)
        except :
            pass
    try:
        next = driver.find_element(By.XPATH, f'//*[@id="pagerTagAnchor{next_number}"]/em')
        if next.text == '다음':
            next.click()
            next_number += 1
            time.sleep(0.1)
        else :
            next_onoff = False
    except:
        next_onoff = False