
import time
import json
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--headless")  # Chạy ẩn
options.add_argument("--disable-gpu")  # Tắt GPU tăng hiệu suất (Windows)
options.add_argument("--no-sandbox")

def get_contents(body): 
    sumary = driver.find_element(By.CLASS_NAME, "the-article-summary") # lọc tổng kết
    try:
        contents = body.find_elements(By.XPATH, "./p") # lọc lấy phần content, không lấy nội dung của các nội dung con
        contents.insert(0, sumary) 
        all_contents = []
        for content in contents:
            all_contents.append(content.text) # chuyển đổi từ webdriver sang text
        result = "/n".join(all_contents) # convert từ list sang string
        return result
    except:
        return sumary.text # nếu không có content nào thì chỉ có sumary thôi

def get_img(body):
    actions = ActionChains(driver) # tạo hoạt động cuộn chuột
    # việc tạo hành động cuộn chuột để tránh trường hợp không load được ảnh, vì nếu ko load được thì sẽ không lấy được link
    for _ in range(10):  # Cuộn 10 lần
        actions.scroll_by_amount(0, 600).perform()  # Cuộn xuống 100px
        time.sleep(0.3) # nghỉ
    pictures = body.find_elements(By.CLASS_NAME, "z-photoviewer-wrapper")
    pic_cap = []
    #tìm ảnh
    for picture in pictures:
        link = ""
        pics = picture.find_elements(By.CLASS_NAME, "pic")
        for pic in pics:
            imgs = pic.find_elements(By.TAG_NAME, "img")
            for img in imgs:
                link = link + img.get_attribute("src") + ", "
        cap = picture.text # vì việc tìm cap của ảnh rất loằn ngoằn nên ở đây chuyển đổi ảnh thành dạng text sẽ có luôn cap của ảnh
        pic_cap.append([link,cap])
    return pic_cap


with open("/home/rmie/Desktop/crawling/Links/links_phapluat.txt", "r", encoding="utf-8") as file: #đọc file txt
    links = file.readlines()  # Đọc tất cả các dòng vào danh sách
    links = [line.strip() for line in links]  # Loại bỏ ký tự xuống dòng
# links là danh sách link các bài báo
cnt = 142 # để đếm số lương cũng như là stt của file json
for link in links:
    if cnt >= 200: break

    chrome_service = Service('/home/rmie/Desktop/crawling/chromedriver')
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.get(link)
    time.sleep(2)
    
    url = link # link web
    title = driver.find_element(By.CLASS_NAME, "the-article-title")
    #lọc chỉ lấy phần body( nội dung ) của bài báo
    body = driver.find_element(By.CLASS_NAME, "the-article-body") 
    contents = get_contents(body)
    img = get_img(body)
    # convert tất cả về dạng dict
    result = {
    "url": link, 
    "title": title.text, 
    "content": contents, 
    "metadata": img
    }
    #cuối cùng là lưu dict về dạng json
    stt = str(cnt) + ".json"
    path = "/home/rmie/Desktop/crawling/Zingnews/Phapluat/" + stt
    with open(path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    cnt += 1
    driver.quit()


    
