from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd
import xlwt
import openpyxl
import os

def kospi():
    #코스피 주가
    # 크롬 드라이버로 브라우저 열기
    path = "/Users/jaminkim/python/chromedriver"
    driver = webdriver.Chrome(path)

    driver.get("https://m.stock.naver.com/index.html#/domestic/capitalization/KOSPI")
        
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, "html.parser")

    no = 1

    while True:  
        try:
            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[%s]/td[1]/span[1]' %no).click() # 종목 클릭
            time.sleep(1)
        except AttributeError:
            # 더보기
            try:
                body = driver.find_element_by_class_name("international")
                body.send_keys(Keys.PAGE_DOWN)
                driver.find_element_by_class_name("VMore_link__1zqGi").click()
                time.sleep(1)
            except Exception:
                continue

        else:
            driver.find_element_by_xpath('//*[@id="common_component_tab"]/div/ul/li[4]/a').click() # 시세 클릭
            # 갯수만큼 더보기
            cnt = 1
            while True:
                try:
                    body = driver.find_element_by_class_name("international")
                    body.send_keys(Keys.PAGE_DOWN)
                    driver.find_element_by_class_name("VMore_link__1zqGi").click()
                    time.sleep(1)
                except Exception:
                    continue
                else:            
                    cnt += 1
                    if cnt == 25:
                        break

            full_html = driver.page_source
            soup = BeautifulSoup(full_html, "html.parser")
            # 테이블 가져오기
            table = soup.select("table")
            table_html = str(table)
            table_list = pd.read_html(table_html)
            summary = pd.DataFrame(table_list[0], columns=["날짜", "종가", "시가", "고가", "저가"])
            driver.back()
            driver.back()
            
            # 파일이 있는 있는 경우 시트 추가
            if not os.path.exists("KOSPI"):
                with pd.ExcelWriter("KOSPI", mode = "w", engine = "openpyxl") as writer:
                    summary.to_excel(writer, sheet_name="{}" .format(no), index = False)
            else:
                with pd.ExcelWriter("KOSPI", mode = "a", engine = "openpyxl") as writer:
                    summary.to_excel(writer, sheet_name="{}" .format(no), index = False)


            no += 1


def kosdaq():
    # 코스닥 주가
    # 크롬 드라이버로 브라우저 열기
    path = "/Users/jaminkim/python/chromedriver"
    driver = webdriver.Chrome(path)

    driver.get("https://m.stock.naver.com/index.html#/domestic/capitalization/KOSDAQ")
        
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, "html.parser")

    no = 1

    while True:  
        try:
            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[%s]/td[1]/span[1]' %no).click() # 종목 클릭
            time.sleep(1)
        except AttributeError:
            # 더보기
            try:
                body = driver.find_element_by_class_name("international")
                body.send_keys(Keys.PAGE_DOWN)
                driver.find_element_by_class_name("VMore_link__1zqGi").click()
                time.sleep(1)
            except Exception:
                continue

        else:
            driver.find_element_by_xpath('//*[@id="common_component_tab"]/div/ul/li[4]/a').click() # 시세 클릭
            # 갯수만큼 더보기
            cnt = 1
            while True:
                try:
                    body = driver.find_element_by_class_name("international")
                    body.send_keys(Keys.PAGE_DOWN)
                    driver.find_element_by_class_name("VMore_link__1zqGi").click()
                    time.sleep(1)
                except Exception:
                    continue
                else:            
                    cnt += 1
                    if cnt == 25:
                        break

            full_html = driver.page_source
            soup = BeautifulSoup(full_html, "html.parser")
            # 테이블 가져오기
            table = soup.select("table")
            table_html = str(table)
            table_list = pd.read_html(table_html)
            summary = pd.DataFrame(table_list[0], columns=["날짜", "종가", "시가", "고가", "저가"])
            driver.back()
            driver.back()
            
            # 파일이 있는 있는 경우 시트 추가
            if not os.path.exists("KOSPI"):
                with pd.ExcelWriter("KOSPI", mode = "w", engine = "openpyxl") as writer:
                    summary.to_excel(writer, sheet_name="{}" .format(no), index = False)
            else:
                with pd.ExcelWriter("KOSPI", mode = "a", engine = "openpyxl") as writer:
                    summary.to_excel(writer, sheet_name="{}" .format(no), index = False)

            no += 1    

kospi()
kosdaq()