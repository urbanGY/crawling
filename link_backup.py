from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
def search_title(title, url, search_xpath):
    try:
        driver.get(url) #default page에 접근
    except:
        print('* except in search_title() : driver.get(url) 에서 url이 잘못됨')
        driver.get(url) #default page에 접근
        driver.implicitly_wait(5) #maxmovie 깉은 경우에는 오래걸림 이게

    elem = driver.find_elements_by_xpath(search_xpath) # 메인 search name
    elem = elem[0] #list object 상태에서는 바로 send Keys를 쓸 수 없다..
    elem.send_keys(Keys.SHIFT + Keys.END) # shift + end 키로 name value를 드레그함
    elem.send_keys(Keys.DELETE) #드레그한 value를 제거해 내가 검색하려는 타이틀만을 깔끔하게 검색하게 만듬
    elem.send_keys(title) #search block에 키워드 입력
    elem.send_keys(Keys.RETURN) #엔터 입력

def remove_blank(s): #입력 스트링의 공백 제거
    remove = ''
    for c in s:
        if c == '\n' or c == '(': # 보통 괄호는 한글 제목의 영문을 표기하기위해 쓰임으로 필터링 결정
            break;
        if c != ' ':
            remove += c
    return remove

def title_cmp(a, b): #두 공백이 제거된 스트링이 같다면 참, 아니면 거짓
    a = remove_blank(a)
    b = remove_blank(b)
    if a == b:
        return True
    else :
        return False

def contry_cmp(conrty, c_contry):
    if contry in c_contry:
        return True
    else :
        return False

def year_cmp(year, open_year, start_year):
    #비교 로직
    return True


#title, open_year, start_year, contry
#title_xpath, year_xpath, contry_xpath
def get_url(title, contry, open_year, start_year, title_xpath, contry_xpath, year_xpath):
    a = driver.find_elements_by_xpath(title_xpath) #anchor title_xpath 객체 생성
    candidate_list = [] # 매칭 후보자 인덱스 리스트
    for i in range(len(a)):
        text = a[i].text
        if title_cmp(title, text):
            candidate_list.append(i)
    if len(candidate_list) == 1: #만약 매칭된 리스트가 단 한개라면
        content_url = a[candidate_list[0]].get_attribute('href') #경로 추출
        driver.get(content_url) # 타겟으로하는 페이지 링크를 잘 찾아왔는지 검사하기위해 여기에 위치
        return content_url #경로 반환

    print('len : ',len(candidate_list))
    c = driver.find_elements_by_xpath(contry_xpath) # 후보자들 중 나라 텍스트 매칭
    for i in candidate_list:
        print('i : ',i)
        c_contry = c[i].text
        if not(contry_cmp(contry, c_contry)): #매칭이 안되었다면
            candidate_list.remove(i) # 후보자에서 제거
    if len(candidate_list) == 1: #만약 매칭된 리스트가 단 한개라면
        content_url = a[candidate_list[0]].get_attribute('href') #경로 추출
        driver.get(content_url) # 타겟으로하는 페이지 링크를 잘 찾아왔는지 검사하기위해 여기에 위치
        return content_url #경로 반환

    y = driver.find_elements_by_xpath(year_xpath) # 개봉 또는 제작 년도 매칭
    for i in candidate_list:
        year = y[i].text
        if not(year_cmp(year, open_year, start_year)): # 개봉, 제작 년도 모두 다르다면
            candidate_list.remove(i)
    if len(candidate_list) == 1:
        content_url = a[candidate_list[0]].get_attribute('href') #경로 추출
    else :
        content_url = ''
    driver.get(content_url) # 타겟으로하는 페이지 링크를 잘 찾아왔는지 검사하기위해 여기에 위치
    return content_url #경로 반환


def get_score(score_xpath):
    try:
        s = driver.find_elements_by_xpath(score_xpath) #score xpath로 해당 elements 추출
        score = extract_score(s[0].text)
        if score == '':
            score = 'not exist'
    except:
        score = 'not exist'
    return score

def extract_score(s): # 순수하게 평점만 추출하는 함수
    score = s
    for i in range(len(s)):
        if s[i] == '\n':
            break
        if s[i] == '.':
            score = s[i-1:i+2]
    return score

def score_scaling(score, scale):
    tmp = score
    try:
        if scale == '5':
            score = float(score)*2.0
    except:
        score = tmp
    return str(score)

chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
chrome_option.add_argument('headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('lang=ko_KR') #selenium 에서 gui 작동 안하게 headless 옵션 달아줌
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
driver.implicitly_wait(3) #랜더링 완료 시간 대기

f = open('data/movie/site_list.json',mode='r',encoding='utf-8')
json_site = json.load(f)
site_list = json_site['site_list']
f.close()
#Todo : movie list 받아서 읽기 준비, movie list 3001 ~ 끝까지 크롤링하자
#Todo : headless 있고 없고에 따라서 max movie를 받고 못받고가 정해지는데 뭐때문일까?
#Todo : 위에 cmp 체워 넣기, xpath 체워넣기, 테스트 코드 작성하기

movie_list = ['엑시트']
for movie in movie_list: # 영화 리스트 순회
    title = movie
    open_year = '2019'
    start_year = '2018'
    contry = '한국'
    json_file = OrderedDict()
    json_file['title'] = title
    link_list = []
    for site in site_list: # 이 카테고리에 해당하는 사이트들 순회
        site_name = site['site_name'] # 사이트명
        scale_type = site['scale_type'] # 평점 스케일
        default_url = site['site_url'] # 사이트 기본 주소
        search_xpath = site['search_xpath'] # 사이트 검색 기능 속성명
        title_xpath = site['title_xpath'] # 기본 주소에서 타이틀로 검색한 결과 리스트 접근 title_xpath
        contry_xpath = site['contry_xpath']
        year_xpath = site['year_xpath'] #  year 접근
        score_xpath = site['score_xpath'] # 별점 접근 속성

        try:
            try: #기존 타이틀 명으로 검색
                search_title(title, default_url, search_xpath)
                content_url = get_url(title, contry ,open_year, start_year, title_xpath, contry_xpath, year_xpath)
            except: #연도를 붙여서 타이틀 검색
                print('* except in get_url() : content_url 을 못 받아옴, title에 year 추가해서 재시도')
                search_title(title + '('+year+')', default_url, search_xpath)
                content_url = get_url(title + '('+year+')', contry ,open_year, start_year, title_xpath, contry_xpath, year_xpath)
        except: #만약 연도를 붙여도 안나온다면
            print('* except in get_url() : get_url() 재시도 실패, '+ site_name + ' crawling은 무시')
            continue
        score = get_score(score_xpath)
        score = score_scaling(score, scale_type)

        json_tmp = OrderedDict()
        json_tmp['site_name'] = site_name
        json_tmp['url'] = content_url
        json_tmp['rating'] = score
        link_list.append(json_tmp)

        print('site name : ',site_name)
        print('url : ',content_url)
        print('raing : ',score)

    json_file['links'] = link_list

    with open('data/movie/output/'+title+'_link.json', 'w', encoding='utf-8') as make_file:
        json.dump(json_file, make_file, ensure_ascii=False, indent="\t")
