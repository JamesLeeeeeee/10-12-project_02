from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time 
import os
import urllib

insta_dict = {'id':[],
              'location': [],
              'date': [],
              'like': [],
              'text': [],
              'hashtag': [],
              'img': []}

    #브라우저 열기
def insta_open(driver):
    login_url = "https://www.instagram.com/accounts/login"
    driver.get(login_url)
    driver.maximize_window() # 전체 화면
    time.sleep(2)

# 로그인 하기
def insta_login(driver):
    driver.find_element_by_name("username").send_keys("teamproject2__")
    instagram_pw_form = driver.find_element_by_name("password").send_keys("projectteam2")
    time.sleep(10)   
    driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF ").click()
    time.sleep(2)

# 이미지 크롤링        
def img_crawl(driver):
    global insta_dict

    # img src 추출    
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        img = soup.find("div", "KL4Bh").find_all("img")
        for i in img:
            img_src = i["src"]
            insta_dict['img'].append(img_src)
    except NoSuchElementException:
        img_src = "none"
        insta_dict['img'].append(img_src)
    else:
        insta_dict['img'].append(img_src)

            
def id_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # id 추출
    try:
        id = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/span').text
    except NoSuchElementException:
        id = "none"
        insta_dict['id'].append(id)
    else:
        insta_dict['id'].append(id)


def text_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        txt = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span').text
    except NoSuchElementException:
        txt = "none"
        insta_dict['text'].append(txt)
    else:
        insta_dict['text'].append(txt)

def hashtag_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        hashtags = soup.find_all('a', class_ = 'xil3i')
    except NoSuchElementException:
        hashtag = 'none'
        insta_dict['hashtag'].append(hashtag)
    else:
        for i in hashtags:
            hashtag = i.text
            insta_dict['hashtag'].append(hashtag)
        
def location_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        location = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[2]/div[2]').text
    except NoSuchElementException:
        location = 'None'
        insta_dict['location'].append(location)
    else:
        insta_dict['location'].append(location)

        
def like_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        # 좋아요수 추출
        like = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/a').text
    except NoSuchElementException:
        try:
            # 동영상인 경우 조회수 추출
            like = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/span').text
        except NoSuchElementException:
            like = 'None'
            insta_dict['like'].append(like)
        else:
            insta_dict['like'].append(like)
    else:
        insta_dict['like'].append(like)


def date_crawl(driver):
    global insta_dict

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    try:
        uploadTime=driver.find_element_by_css_selector('time._1o9PC')
        time=uploadTime.get_attribute('datetime')[:10]
    except:
        time = "none"
        insta_dict['date'].append(time)
    else:
        insta_dict['date'].append(time)


def save_data(kwd):
    global insta_dict

    # 수집한 데이터를 json file로 저장
    with open('instagram_data_{}.json' .format(kwd), 'w') as f:
                    json.dump(insta_dict, f, indent=4) 
    print(insta_dict)
        
        
