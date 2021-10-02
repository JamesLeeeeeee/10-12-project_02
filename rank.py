#https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blUw&qvt=0&query=%EC%9D%BC%EA%B0%84%EC%98%88%EB%8A%A5%20%EC%8B%9C%EC%B2%AD%EB%A5%A0
import pandas as pd

table=pd.read_html('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%93%9C%EB%9D%BC%EB%A7%88+%EC%8B%9C%EC%B2%AD%EB%A5%A0',header=0)
print(table)  
################################
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://finance.naver.com/item/main.nhn?code=035720' # 카카오(035720) 네이버 금융 홈페이지 주소
html = requests.get(url).text
soup = BeautifulSoup(html)
table_html = soup.find('table', {'class' : 'tb_type1 tb_num tb_type1_ifrs'})   # 특정 테이블 태그를 가져옴     
table_html = str(table_html)      # 'table'변수는 bs4.element.tag 형태이기 때문에 table를 문자열 형태로 바꿔준다  

table_df_list = pd.read_html(table_html)   # read_html 사용해서 html을 데이터프레임들로 이루어진 리스트로 바꿔줌  
table_df = table_df_list[0]    # 원하는 데이터프레임을 가져온다  

print(table_df)