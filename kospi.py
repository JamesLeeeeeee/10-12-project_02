from datetime import date
from selenium import webdriver #크롤링을 위한 셀레니움 웹드라이버
import time  #시간, 슬립을 위한 타임
import pandas as pd


titles = []
dates = []
cp = []
ftr = []
fr = []
tv = []
ta = []
indi = []
frs = []
inst = []

print ("-------코스피 크롤링 Ver 0.1---------")
print ("기본적으로 오늘로 부터 2년간의 데이터를 추출합니다.")

w_path = "C:\python_temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(w_path)
driver.get("https://finance.daum.net/domestic/kospi")  #다음 코스피 기준
time.sleep(5)  #페이지 로딩 5초 기다림

theads = driver.find_elements_by_xpath('//*[@id="boxDailyHistory"]/div[2]/div/table/thead/tr/th') #컬럼 타이틀

#컬럼 타이틀 출력
for thead in theads:
    print(f'{thead.text:^7}', end='|')
    titles.append(thead.text)
print('\n'+'-'*120)


#일자별 영역 
data_area = driver.find_element_by_id('boxDailyHistory')
start_day=driver.find_element_by_xpath('//*[@id="boxDailyHistory"]/div[2]/div/table/tbody/tr[1]/td[1]/span').text #시작년월일
end_day=str(int(start_day[0:2])-2)+start_day[2:]   #마지막년월일 
#데이터 출력
for day10 in range(((365*2)-2*104)//10): #10일별 페이지 이동 (2년 - 104주간 주말 뺀 일수//10)
    

    trs = driver.find_elements_by_xpath('//*[@id="boxDailyHistory"]/div[2]/div/table/tbody/tr') #페이지당 10일치
    for i in range(1,len(trs)+1):
        tdpath = f'//*[@id="boxDailyHistory"]/div[2]/div/table/tbody/tr[{i}]/td'
        tds = driver.find_elements_by_xpath(tdpath)
        
        dates.append(tds[0].text)
        cp.append(tds[1].text)
        ftr.append(tds[2].text)
        fr.append(tds[3].text)
        tv.append(tds[4].text)
        ta.append(tds[5].text)
        indi.append(tds[6].text)
        frs.append(tds[7].text)
        inst.append(tds[8].text)
        
        for td in tds:
            print(f'{td.text:^10}', end='|')
            
        print()
        
        if tds[0].text == end_day: break  #2년전 날짜면 탈출
    
    if tds[0].text == end_day: break #2년전 날짜면 탈출
    
    
    # driver.find_element_by_xpath(f'//*[@id="boxDailyHistory"]/div[2]/div/div/a[{day10+1}]').click()  #0일때 2번페이지클릭
    
    if (day10+1)%10==0:  #10페이지마다 > 다음페이지들 가져오기
        data_area.find_element_by_link_text('다음').click()
    else:
        next_page=str(day10+2) #0일때 2번눌러야하므로
        data_area.find_element_by_link_text(next_page).click() 
    
    time.sleep(2)

data = pd.DataFrame()
data['일자'] = dates
data['종가'] = cp 
data['전일비'] = ftr 
data['등락률'] = fr
data['거래량'] = tv
data['거래대금'] = ta
data['개인(억)'] = indi
data['기관(억)'] = inst
data['외국인(억)'] = frs
data = data.set_index('일자')
data.to_excel("kospi_result.xlsx")

# while True:
    

print("출력 완료")
driver.close()