

import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time



driver = webdriver.Chrome('chromedriver')


driver.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=74977')

try:
    explanation_Se = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[4]/div[1]/div/div[1]/p')
    content = explanation_Se.text

    print(content)
except:
    print("explation not found")