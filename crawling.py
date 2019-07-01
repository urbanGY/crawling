#movie site list { 왓챠, 네이버, 로튼토마토 등등..}
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getScore(s):
    score = ''
    for i in range(len(s)):
        if s[i] == '.':
            score += s[i-1:i+2]
    return score

url = 'https://watcha.com/ko-KR' #crawling 하려는 사이트 url
keyWord = '아이언맨1' #항목 생성하려는 대상 이름

xpath_watcha = '//*[@id="root"]/div/div[1]/section/section/section[2]/div[2]/div[1]/div/div/div/ul/li[1]/a' #watcha 사이트의 세부 정보 링크 xpath

chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
chrome_option.add_argument('headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('lang=ko_KR') #selenium 에서 gui 작동 안하게 headless 옵션 달아줌

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
driver.implicitly_wait(3) #랜더링 완료 시간 대기
driver.get(url)

#whatcha의 메인 검색 페이지
elem = driver.find_element_by_name('search') # 왓챠의 메인 search name
elem.send_keys(keyWord) #search block에 키워드 입력
elem.send_keys(Keys.RETURN) #엔터 입력

#검색된 페이지에서 keyword에 해당하는 항목 선택
#TODO: 영화 항목에서 이름 매칭을 통해서 해당 디렉토리로 이동하게 하기
a = driver.find_elements_by_xpath(xpath_watcha) #anchor xpath 객체 생성
driver.get(a[0].get_attribute('href')) #해당 객체에서 href 경로로 이동

#keyword 세부 정보 페이지
req = driver.page_source
page = BeautifulSoup(req, 'html.parser') #html 넘기기
info = page.select('div.css-ag7vr6-ContentRatings.e1sxs7wr16') #별점 div 특정
s = info[0].text #string 추출
score = getScore(s) #score만 추출하기

print('%s 의 평점은 %s 점 입니다!'%(keyWord,score))
