import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service

chrome_service = Service('/home/rmie/Desktop/crawling/chromedriver')
driver = webdriver.Chrome(service=chrome_service)
driver.get("https://znews.vn/bong-da-viet-nam.html")
time.sleep(5)


def checkyear(article): # hàm kiểm tra năm của bài báo xem có hợp lệ khong ? hàm sẽ đưa vào một article của 1 content lớn( nơi chưa cả nội dung và ngày tháng bla bla)
    dateweb = article.find_element(By.CLASS_NAME, "date") # ở đây nó sẽ lọc ra phần ngày tháng của bài báo
    date = dateweb.text # chuyển đổi sang dạng text
    print(date)
    try: # tránh những trường hợp bị lỗi data
        a,b,c = date.split('/')
        return c
    except: return False

if '__name__' == '__name__':
    last_height = driver.execute_script("return document.body.scrollHeight") # lưu độ cao của trang web hiện tại
    links = set()
    while True:
        box = driver.find_element(By.ID, "news-latest") # tim hộp tin mới
        content_box = box.find_element(By.CLASS_NAME, "section-content") # tìm hộp content
        contents = content_box.find_elements(By.CLASS_NAME, "article-item") # tìm tất cả các content lớn có trong contentbox
        contents_rev = contents[::-1] #đảo ngược list để tiết kiếm thời gian duyệt
        for content in contents_rev: # duyệt qua từng content trong đó
            if checkyear(content) == "2025": break #nếu là năm 2025 thì out vì đang cần năm 2024
            else:
                if checkyear(content) == "2024": # kiểm tra năm
                    linkbox = content.find_element(By.CLASS_NAME, "article-thumbnail") # tìm link
                    linkline= linkbox.find_element(By.CSS_SELECTOR, 'a')
                    link = linkline.get_attribute('href')
                    links.add(link) # có link rồi thì nhét vô set
            if checkyear(content) == "2023": break # nếu qua năm 2024 rồi thì cook
        if len(links) >= 200: break # vì chỉ lấy 200 bài viết thôi
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # cuộn xuống cuối trang
        time.sleep(3) #ngưng để load nội dung
        new_height = driver.execute_script("return document.body.scrollHeight") # cập nhập độ cao mới
        if new_height == last_height: # nếu độ cao không thay đổi thì kết thúc
            break
        last_height = new_height

    results = list(links) # convert từ set sang list để lưu kết quả xuống
    with open("links_thethao.txt", "w") as f:
        for item in results:
            f.write(item + "\n")

    driver.quit()