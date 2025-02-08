from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import time

# Cấu hình Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ở chế độ không hiển thị trình duyệt
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_service = Service('/home/rmie/Desktop/crawling/chromedriver')  # Thay thế bằng đường dẫn tới chromedriver của bạn

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get('https://lifestyle.znews.vn/giao-duc.html')

# Hàm kiểm tra năm của bài viết
def is_article_in_year(article, year):
    try:
        date_text = article.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
        article_date = datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
        return article_date.year == year
    except Exception as e:
        return False

# Danh sách lưu trữ các bài viết
articles_2024 = []

# Số lần cuộn tối đa
max_scrolls = 50
scroll_pause_time = 2  # Thời gian chờ sau mỗi lần cuộn

for _ in range(max_scrolls):
    # Tìm tất cả các bài viết hiện tại trên trang
    articles = driver.find_elements(By.CSS_SELECTOR, 'article')

    for article in articles:
        if is_article_in_year(article, 2024):
            title = article.find_element(By.CSS_SELECTOR, 'h3').text
            link = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            articles_2024.append({'title': title, 'link': link})

    # Cuộn xuống cuối trang
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# Loại bỏ các bài viết trùng lặp
unique_articles = {v['link']: v for v in articles_2024}.values()

# In ra các bài viết thu thập được
for article in unique_articles:
    print(f"Title: {article['title']}, Link: {article['link']}")

# Đóng trình duyệt
driver.quit()
