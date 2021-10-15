from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import os
import urllib

class Instagram:
    #브라우저 열기
    def insta_open(self):
        driver_path = "/Users/jaminkim/python/chromedriver"
        self.driver = webdriver.Chrome(driver_path)
        login_url = "https://www.instagram.com/accounts/login"
        self.driver.get(login_url)
        self.driver.maximize_window() # 전체 화면
        time.sleep(1)
        time.sleep(2)

    # 로그인 하기
    def insta_login(self):
        self.driver.find_element_by_name("username").send_keys("__teamproject2__")
        instagram_pw_form = self.driver.find_element_by_name("password").send_keys("projectteam2")     
        self.driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF ").click()
        time.sleep(2)

    #     pickle.dump(driver.get_cookies(), open("instacookie.txt", "wb"))
    
    # 더보기 누르기
    def popup(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click() # 나중에 하기
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click() # 나중에 하기

    # 검색하기
    def search(self):
        element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')# 검색
        element.clear()
        element.send_keys("맛집")
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)

class Insta_crawler(Instagram)from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import os
import urllib
import pandas as pd

class Instagram:
    #브라우저 열기
    def insta_open(self):
        driver_path = "/Users/jaminkim/python/chromedriver"
        self.driver = webdriver.Chrome(driver_path)
        login_url = "https://www.instagram.com/accounts/login"
        self.driver.get(login_url)
        self.driver.maximize_window() # 전체 화면
        time.sleep(1)
        time.sleep(2)

    # 로그인 하기
    def insta_login(self):
        self.driver.find_element_by_name("username").send_keys("teamproject2__")
        instagram_pw_form = self.driver.find_element_by_name("password").send_keys("projectteam2")     
        self.driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF ").click()
        time.sleep(2)

    #     pickle.dump(driver.get_cookies(), open("instacookie.txt", "wb"))
    
    # 더보기 누르기
    def popup(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click() # 나중에 하기
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click() # 나중에 하기

    # 검색하기
    def search(self):
        element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')# 검색
        element.clear()
        element.send_keys("맛집")
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)

class Insta_crawler(Instagram):
    global img_l
    global account_l
    global txt_l
    global hashtag_l
    global location_l
    global like_l
    global view_l

    # 크롤링
    account_l = []
    img_l = []
    txt_l = []
    hashtag_l = []
    location_l = []
    like_l = []
    view_l = []
    
    def setting(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 스크롤 다운
        time.sleep(1)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")
        self.div = self.soup.find_all("KC1QD")
        
    def img_crawl(self):
        
        img_src = self.soup.find("KC1QD").find_all("img")
        print(self.soup)
        print()
        print(img_src)
        for i in img_src:
            img_src1 = i["src"]
            img_l.append(img_src1)
            
    def account_crawl(self):
        account = self.div.find_element_by_xpath("/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span")
        account_l.append(account.text)
        
    def text_crawl(self):
        txt = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span")
        txt_l.append(txt.text)
        
    def hashtag_crawl(self):
        hashtag = self.div.find_all("xil3i")
        hashtag_l.append(hashtag.text)
        
        
    def location_crawl(self):
        location = self.div.find_element_by_xpath("/div[2]/div/div/div[1]/div/header/div[2]/div[2]/div[2]")
        location_l.append(location.text)
        
    def like_crawl(self):
        like = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/div/a/span")
        like_l.append(like.text)
        
    def view_crawl(self):
        view = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/span/span")
        view_l.append(view)

class Save_file:
    def save_img(self):
        # file 생성
        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d-%02d" %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.f_dir = "/Users/jaminkim/python/" + f_name
        if not os.path.exists(self.f_dir):
            os.makedirs(self.f_dir)
            os.chdir(self.f_dir)
        else:
            os.removedirs(self.f_dir)
            os.makedirs(self.f_dir)

        file_no = 1
        for i in range(0, len(img_l)):
            urllib.request.urlretrieve(img_l[i], str(file_no)+".jpg")
            file_no += 1

    def save_xls(self):
        result = pd.DataFrame()
        result["account"] = account_l
        result["text"] = txt_l
        result["hashtag"] = hashtag_l
        result["location"] = location_l
        result["like"] = like_l
        result["view"] = view_l

        result.to_excel(self.f_dir + ".xls")
        
        
class Run(Insta_crawler):
    
    def run(self):
        self.insta_open()
        self.insta_login()
        try:
            self.popup()
        except Exception:
            pass
        self.search()
        self.setting()
        while len(img_l) <= 20:
            self.img_crawl()
            self.save_img()

        cnt = 1    
        while cnt <= 20:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[{}]/a/div/div[2]' .format(cnt)).click() # 게시물 클릭
            self.account_crawl()
            try:
                self.txt_crawl()
            except AttributeError:
                pass
            try:
                self.hashtag_crawl()
            except AttributeError:
                pass
            try:
                self.location_crawl()
            except AttributeError:
                pass
            try:
                self.like_crawl()
            except AttributeError:
                pass
            try:
                self.view_crawl()
            except AttributeError:
                pass
            self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/button").click() # 닫기
            cnt += 1
        
        self.save_xls():
    global img_l
    global account_l
    global txt_l
    global hashtag_l
    global location_l
    global like_l
    global view_l

    # 크롤링
    account_l = []
    img_l = []
    txt_l = []
    hashtag_l = []
    location_l = []
    like_l = []
    view_l = []
    
    def setting(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 스크롤 다운
        time.sleep(1)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import os
import urllib
import pandas as pd

class Instagram:
    #브라우저 열기
    def insta_open(self):
        driver_path = "/Users/jaminkim/python/chromedriver"
        self.driver = webdriver.Chrome(driver_path)
        login_url = "https://www.instagram.com/accounts/login"
        self.driver.get(login_url)
        self.driver.maximize_window() # 전체 화면
        time.sleep(1)
        time.sleep(2)

    # 로그인 하기
    def insta_login(self):
        self.driver.find_element_by_name("username").send_keys("teamproject2__")
        instagram_pw_form = self.driver.find_element_by_name("password").send_keys("projectteam2")     
        self.driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF ").click()
        time.sleep(2)

    #     pickle.dump(driver.get_cookies(), open("instacookie.txt", "wb"))
    
    # 더보기 누르기
    def popup(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click() # 나중에 하기
        time.sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click() # 나중에 하기

    # 검색하기
    def search(self):
        element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')# 검색
        element.clear()
        element.send_keys("맛집")
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(2)

class Insta_crawler(Instagram):
    global img_l
    global account_l
    global txt_l
    global hashtag_l
    global location_l
    global like_l
    global view_l

    # 크롤링
    account_l = []
    img_l = []
    txt_l = []
    hashtag_l = []
    location_l = []
    like_l = []
    view_l = []
    
    def setting(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 스크롤 다운
        time.sleep(1)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")
        self.div = self.soup.find_all("KC1QD")
        
    def img_crawl(self):
        
        img_src = self.soup.find("KC1QD").find_all("img")
        print(self.soup)
        print()
        print(img_src)
        for i in img_src:
            img_src1 = i["src"]
            img_l.append(img_src1)
            
    def account_crawl(self):
        account = self.div.find_element_by_xpath("/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span")
        account_l.append(account.text)
        
    def text_crawl(self):
        txt = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span")
        txt_l.append(txt.text)
        
    def hashtag_crawl(self):
        hashtag = self.div.find_all("xil3i")
        hashtag_l.append(hashtag.text)
        
        
    def location_crawl(self):
        location = self.div.find_element_by_xpath("/div[2]/div/div/div[1]/div/header/div[2]/div[2]/div[2]")
        location_l.append(location.text)
        
    def like_crawl(self):
        like = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/div/a/span")
        like_l.append(like.text)
        
    def view_crawl(self):
        view = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/span/span")
        view_l.append(view)

class Save_file:
    def save_img(self):
        # file 생성
        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d-%02d" %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.f_dir = "/Users/jaminkim/python/" + f_name
        if not os.path.exists(self.f_dir):
            os.makedirs(self.f_dir)
            os.chdir(self.f_dir)
        else:
            os.removedirs(self.f_dir)
            os.makedirs(self.f_dir)

        file_no = 1
        for i in range(0, len(img_l)):
            urllib.request.urlretrieve(img_l[i], str(file_no)+".jpg")
            file_no += 1

    def save_xls(self):
        result = pd.DataFrame()
        result["account"] = account_l
        result["text"] = txt_l
        result["hashtag"] = hashtag_l
        result["location"] = location_l
        result["like"] = like_l
        result["view"] = view_l

        result.to_excel(self.f_dir + ".xls")
        
        
class Run(Insta_crawler):
    
    def run(self):
        self.insta_open()
        self.insta_login()
        try:
            self.popup()
        except Exception:
            pass
        self.search()
        self.setting()
        while len(img_l) <= 20:
            self.img_crawl()
            self.save_img()

        cnt = 1    
        while cnt <= 20:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[{}]/a/div/div[2]' .format(cnt)).click() # 게시물 클릭
            self.account_crawl()
            try:
                self.txt_crawl()
            except AttributeError:
                pass
            try:
                self.hashtag_crawl()
            except AttributeError:
                pass
            try:
                self.location_crawl()
            except AttributeError:
                pass
            try:
                self.like_crawl()
            except AttributeError:
                pass
            try:
                self.view_crawl()
            except AttributeError:
                pass
            self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/button").click() # 닫기
            cnt += 1
        
        self.save_xls()
        self.div = self.soup.find_element_by_xpath("/html/body/div[6]/div[2]/div/article/div")
        
    def img_crawl(self):
        
        img_src = self.soup.find("KC1QD").find_all("img")
        print(self.soup)
        print()
        print(img_src)
        for i in img_src:
            img_src1 = i["src"]
            img_l.append(img_src1)

    def save_img(self):
        # file 생성
        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d-%02d" %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        f_dir = "/Users/jaminkim/python/" + f_name
        if not os.path.exists(f_dir):
            os.makedirs(f_dir)
            os.chdir(f_dir)
        else:
            os.removedirs(f_dir)
            os.makedirs(f_dir)

        file_no = 1
        for i in range(0, len(img_l)):
            urllib.request.urlretrieve(img_l[i], str(file_no)+".jpg")
            file_no += 1
            
    def account_crawl(self):
        account = self.div.find_element_by_xpath("/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span")
        account_l.append(account.text)
        
    def text_crawl(self):
        txt = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span")
        txt_l.append(txt.text)
        
    def hashtag_crawl(self):
        hashtag = self.div.find_all("xil3i")
        hashtag_l.append(hashtag.text)
        
        
    def location_crawl(self):
        location = self.div.find_element_by_xpath("/div[2]/div/div/div[1]/div/header/div[2]/div[2]/div[2]")
        location_l.append(location.text)
        
    def like_crawl(self):
        like = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/div/a/span")
        like_l.append(like.text)
        
    def view_crawl(self):
        view = self.div.find_element_by_xpath("/div[2]/div/div/div[2]/section[2]/div/span/span")
        view_l.append(view)
        
        
class Run(Insta_crawler):
    
    def run(self):
        self.insta_open()
        self.insta_login()
        self.popup()
        self.search()
        self.setting()
        while len(img_l) <= 20:
            self.img_crawl()
            self.save_img()

        cnt = 1    
        while cnt <= 20:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[{}]/a/div/div[2]' .format(cnt)).click() # 게시물 클릭
            self.account_crawl()
            try:
                self.txt_crawl()
            except AttributeError:
                pass
            try:
                self.hashtag_crawl()
            except AttributeError:
                pass
            try:
                self.location_crawl()
            except AttributeError:
                pass
            try:
                self.like_crawl()
            except AttributeError:
                pass
            try:
                self.view_crawl()
            except AttributeError:
                pass
            self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/button").click() # 닫기
            cnt += 1
