from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import os
import urllib
import pandas as pd

insta_dict = {
        "account" : [],
        "img" : [],
        "txt" : [],
        "hashtag" : [],
        "location" : [],
        "like" : [],
        "view" : [],
        "date" : []
    }

def insta_login(driver):
    driver.find_element_by_name("username").send_keys("teamproject2__")
    instagram_pw_form = driver.find_element_by_name("password").send_keys("projectteam2")     
    driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF ").click()
    time.sleep(2)

def popup(driver):
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click() # 나중에 하기
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click() # 나중에 하기
    time.sleep(1)

def search(driver):
    kwd = input("검색어를 입력하세요 : ")
    element = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')# 검색
    element.clear()
    element.send_keys(kwd)
    time.sleep(2)
    element.send_keys(Keys.ENTER)
    time.sleep(2)
    element.send_keys(Keys.ENTER)
    time.sleep(2)

def img_crawl(soup):      
    img_src = soup.find("KL4Bh").find_all("img")["src"]
    insta_dict['img'].append(img_src)

def account_crawl(driver):
    account = driver.find_element_by_css_selector('h2._6lAjh').text
    insta_dict['account'].append(account.text)

def text_crawl(driver):
    try:
        txt = div.find_element_by_xpath("/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span").text
        insta_dict['txt'].append(txt.text)
    except AttributeError:
        txt = "내용이 없습니다."
    
def hashtag_crawl(driver):
    try:
        hashtag = div.find_all("xil3i").get_text
        insta_dict['hashtag'].append(hashtag.text)
    except AttributeError:
        hashtag = "내용이 없습니다."

def location_crawl(driver):
    try:
        location = div.find_element_by_xpath("/div[2]/div/div/div[1]/div/header/div[2]/div[2]/div[2]").text
        insta_dict['location'].append(location.text)
    except AttributeError:
        location = "내용이 없습니다."

def like_crawl(driver):
    try:
        like = div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/div/a/span").text
        insta_dict['like'].append(like.text)
    except AttributeError:
        like = "내용이 없습니다."

def view_crawl(driver):
    try:
        view = div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/span/span").text
        insta_dict['view'].append(view)
    except AttributeError:
        view = "내용이 없습니다."

def date_crawl(driver):
    try:
        date = div.find_element_by_xpath("/html/body/div[6]/div[2]/div/article/div/div[2]/div/div[2]/div[2]/a/time").text
        insta_dict['date'].append(view)
    except AttributeError:
        date = "내용이 없습니다."

def run():
    # 브라우저 열기
    driver_path = "/Users/jaminkim/python/chromedriver"
    driver = webdriver.Chrome(driver_path)
    login_url = "https://www.instagram.com/accounts/login"
    driver.get(login_url)
    driver.maximize_window() # 전체 화면
    time.sleep(1)

    insta_login(driver)
    try:
        popup(driver)
    except Exception:
        pass
    search(driver)
    time.sleep(5)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 스크롤 다운
    time.sleep(1)

    cnt = 1    
    while cnt <= 20:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div').click() # 게시물 클릭
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        img_crawl(soup)
        account_crawl(driver)
        text_crawl(driver)
        hashtag_crawl(driver)
        location_crawl(driver)
        like_crawl(driver)
        view_crawl(driver)
        date_crawl(driver)
        driver.find_element_by_link_text('다음').click() # 다음
        cnt += 1