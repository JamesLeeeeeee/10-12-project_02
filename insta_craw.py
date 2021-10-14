from bs4 import BeautifulSoup
import time
import urllib.request #이미지 저장
from selenium.webdriver.common.keys import Keys #스크롤다운
from selenium.webdriver.common.by import By #By로 html속성 '값'으로 요소찾음
from selenium.webdriver.support import expected_conditions as EC #특정 html코드가 존재하는지 여부체크
from selenium.webdriver.support.ui import WebDriverWait #EC가 뜰때까지 기다림
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException #EC에서 설정한 시간이 지나면 뜨는 에러 exception처리
import json
import random

##데이터를 저장할 Dictionary
insta_dict = {'id':[],
              'location': [],
              'date': [],
              'like': [],
              'text': [],
              'hashtag': [],
              'img': []}

def IG_run(driver):
    ##데이터를 저장할 Dictionary
#     insta_dict = {'id':[],
#                   'location': [],
#                   'date': [],
#                   'like': [],
#                   'text': [],
#                   'hashtag': [],
#                   'img': []}
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
#     search = driver.find_element_by_class_name('XTCLo.x3qfX')
    text = input("검색어 입력")
#     search.send_keys(text)
#     time.sleep(2)
#     search.send_keys(Keys.RETURN)
#     search.send_keys(Keys.RETURN)
    driver.get("https://www.instagram.com/explore/tags/"+text)
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')))
    except TimeoutException:
        pass
    else:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div').click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        no = 1
        runs = True
        while runs:
            print('게시글:',no)
            IG_ID(driver, insta_dict)
            IG_location(driver, insta_dict)
            IG_text(driver, insta_dict)
            IG_like(driver, insta_dict)
            IG_date(driver, insta_dict)
            IG_img(driver, insta_dict, no)
            no += 1
            #다음 게시글 클릭
            time.sleep(1+ random.randrange(1,7))
            driver.find_element_by_link_text('다음').click()

def IG_ID(driver, insta_dict):
    ## 게시자 ID
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'cv3IO')))
    except TimeoutException:
        print("크롤링할 데이터가 없습니다.")
        runs = False
        pass
    else:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        info_id = soup.find('a','sqdOP yWX7d _8A5w5 ZIAjV').get_text()
        print(info_id)
        insta_dict['id'].append(info_id)

def IG_location(driver, insta_dict):
    ## 게시글 위치
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        info_location = soup.find('a','O4GlU').get_text()
    except AttributeError:
        info_location = '장소정보없음'
        insta_dict['location'].append(info_location)
        print('장소정보가 없습니다.')
    else:
        print(info_location)
        insta_dict['location'].append(info_location)

def IG_text(driver, insta_dict):
    ## 게시글 내용/해시태그 추출
    text = []
    tag = []
    try:
        texts = driver.find_element_by_css_selector('div.C4VMK')
        info_text = texts.find_elements_by_tag_name('span')
    except AttributeError:
        #내용 없을시 각 text, tag리스트에 내용없음 처리
        text.append('내용없음')
        print('내용정보가 없습니다.')
        tag.append('해시태그없음')
        print('해시태그정보가 없습니다.')
    else:
        for i in range(len(info_text)):
            #첫번째는 아이디로 패스
            if i == 0:
                pass
            else:
                #게시글 내용 split()으로 나누기
                texts = info_text[i].text.split()
                for t in texts:
                    # '#'가 들어간 글은 tag리스트에 담기
                    if '#' in t:
                        tag.append(t)
                    # 그 외 text리스트에 담기
                    else:
                        text.append(t)
        #글에 해시태그가 없을 시 해시태그 없음 처리
        if '#' not in info_text[1].text:   
            tag.append('해시태그없음')
    insta_dict['text'].append(text)
    insta_dict['hashtag'].append(tag)
    print(text)
    print(tag)

def IG_like(driver, insta_dict):
    ## 게시글 좋아요정보(사진일 경우) / 조회수정보(동영상일 경우)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        info_like = soup.select_one('div[class="Nm9Fw"] > a[class="zV_Nj"]').get_text()
    except AttributeError:
        #좋아요없을 시 조회수 크롤링
        try:
            info_like = soup.find('span','vcOH2').get_text()
        except AttributeError:
            #좋아요, 조회정보 없을 시 모두 없음처리
            info_like = '정보없음'
            insta_dict['like'].append(info_like)
            print('좋아요, 조회수정보가 없습니다.')
        else:
            print(info_like)
            insta_dict['like'].append(info_like)
    else:
        # '여러명'으로 뜰 때 들어가서 좋아요 수 세기
        if '여러' in info_like:
            like = []
            driver.find_element_by_link_text('여러 명').click()
            time.sleep(2)
            while True:
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                #스크롤 높이 구하기
                last_height =driver.find_element_by_xpath('/html/body/div[7]/div/div/div[3]/div/div/div/div/div/div/span/a').location
                likes = driver.find_element_by_class_name('i0EQd')
                likes = likes.find_elements_by_class_name('MBL3Z')
                for i in likes:
                    p = i.get_attribute('title')
                    if p not in like:
                        like.append(p)
                    else:
                        pass
                driver.find_element_by_css_selector('div._1XyCr').click()
                #스크롤 다운
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                #스크롤 높이 다시 구하기
                new_height =driver.find_element_by_xpath('/html/body/div[7]/div/div/div[3]/div/div/div/div/div/div/span/a').location
                if new_height == last_height:
                    break
                last_height = new_height
            print(f'좋아요 {len(like)}개')
            insta_dict['like'].append(f'좋아요 {len(like)}개')
            driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/div/div[2]/button').click()
        else:
            print(info_like)
            insta_dict['like'].append(info_like)
        
def IG_date(driver, insta_dict):
    ##게시시간 추출
    try:
        time = driver.find_element_by_tag_name('time').get_attribute('title')
    except:
        insta_dict['date'].append('시간정보없음')
    else:
        print(time)
        insta_dict['date'].append(time)

def IG_img(driver, insta_dict, no):
    ##이미지 저장
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        post = driver.find_element_by_class_name("PdwC2.fXiEu")
        #이미지 'src' 추출
        info_img = post.find_element_by_css_selector("img.FFVAD").get_attribute('src')
    except NoSuchElementException:
        #동영상일 때 처리하기
        try:
            info_img = soup.find('div','_97aPb')
        except:
            try:
                info_img = soup.find('div','_5wCQW')
            except:
                pass
            else:
                info_img = '사진없음'
                insta_dict['img'].append(info_img)
                print('사진정보가 없습니다.')
        else:
            info_img = '사진없음'
            insta_dict['img'].append(info_img)
            print('사진정보가 없습니다.')
    else:
        insta_dict['img'].append(info_img)
        urllib.request.urlretrieve(info_img, str(f'{no}-{insta_dict["id"][no-1]}.jpg'))
        print(info_img)