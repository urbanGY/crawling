from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
def remove_blank(s): #입력 스트링의 공백 제거
    remove = ''
    for c in s:
        if c == '\n' or c == '(': # 보통 괄호는 한글 제목의 영문을 표기하기위해 쓰임으로 필터링 결정
            break;
        if c != ' ':
            remove += c
    return remove

def remove_cmp(a, b): #두 공백이 제거된 스트링이 같다면 참, 아니면 거짓
    a = remove_blank(a)
    b = remove_blank(b)
    if a == b:
        return True
    else :
        return False

def get_url_score(title, url, search_xpath, list_xpath, score_xpath):
    #whatcha의 메인 검색 페이지
    driver.get(url) #default page에 접근
    elem = driver.find_elements_by_xpath(search_xpath) # 왓챠의 메인 search name
    elem = elem[0] #list object 상태에서는 바로 send Keys를 쓸 수 없다..
    elem.send_keys(title) #search block에 키워드 입력
    elem.send_keys(Keys.RETURN) #엔터 입력

    a = driver.find_elements_by_xpath(list_xpath) #anchor list_xpath 객체 생성
    content_url = ''
    for n in a:
        text = n.text
        if remove_cmp(title, text):
            content_url = n.get_attribute('href')
            break

    driver.get(content_url) #해당 객체에서 href 경로로 이동
    s = driver.find_elements_by_xpath(score_xpath) #score xpath로 해당 elements 추출
    score = get_score(s[0].text)
    return content_url, score #html 넘기기

def get_score(s): # 순수하게 평점만 추출하는 함수
    score = ''
    for i in range(len(s)):
        if s[i] == '\n':
            break
        if s[i] == '.':
            score += s[i-1:i+2]
    return score

def score_scaling(score, scale):
    if scale == '5':
        score = float(score)*2.0
    return str(score)

chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
chrome_option.add_argument('headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('lang=ko_KR') #selenium 에서 gui 작동 안하게 headless 옵션 달아줌
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
driver.implicitly_wait(3) #랜더링 완료 시간 대기

# list read code will located
site_list = [
    {
        'site_name' : 'watcha',
        'scale_type' : '5',
        'site_url' : 'https://watcha.com/ko-KR',
        'search_xpath' : '//*[@id="search_bar_in_home"]',
        'score_xpath' : '//*[@id="root"]/div/div[1]/section/div/div/div/section/div[2]/div/div/div/div/div[2]',
        'list_xpath' :  '//*[@id="root"]/div/div[1]/section/section/section[2]/div[2]/div[1]/div/div/div/ul/li[@*]/a'
    },
    {
        'site_name' : 'naver_movie',
        'scale_type' : '10',
        'site_url' : 'https://movie.naver.com',
        'search_xpath' : '//*[@id="ipt_tx_srch"]',
        'score_xpath' : '//*[@id="actualPointPersentBasic"]/div',
        'list_xpath' : '//*[@id="old_content"]/ul[2]/li[not(@*)]/dl/dt/a'
    }
    # },
    # {
    #     'site_name' : 'daum_movie',
    #     'scale_type' : '10',
    #     'site_url' : 'https://movie.daum.net/main/new#slide-1-0',
    #     'search_xpath' : 'search',
    #     'score_xpath' : 'score',
    #     'list_xpath' : ''
    # },
    # {
    #     'site_name' : 'maxmovie',
    #     'scale_type' : '10',
    #     'site_url' : 'http://search.maxmovie.com/search',
    #     'search_xpath' : 'search',
    #     'score_xpath' : 'score',
    #     'list_xpath' : ''
    # }
]
#Todo : 나머지 두 사이트도 추가, movie list 받아서 읽기 준비, movie list 3001 ~ 끝까지 크롤링하자
movie_list = ['닥터스트레인지']
for movie in movie_list: # 영화 리스트 순회
    title = movie
    json_file = OrderedDict()
    json_file['title'] = title
    link_list = []
    for site in site_list: # 이 카테고리에 해당하는 사이트들 순회
        site_name = site['site_name'] # 사이트명
        scale_type = site['scale_type'] # 평점 스케일
        default_url = site['site_url'] # 사이트 기본 주소
        search_xpath = site['search_xpath'] # 사이트 검색 기능 속성명
        score_xpath = site['score_xpath'] # 별점 접근 속성
        list_xpath = site['list_xpath'] # 기본 주소에서 타이틀로 검색한 결과 리스트 접근 list_xpath

        content_url, score = get_url_score(title, default_url, search_xpath, list_xpath, score_xpath) #html 과 url링크 가져옴
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
