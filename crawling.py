#movie site list { 왓챠, 네이버, 로튼토마토 등등..}
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

def get_html(url, title, xpath_watcha):
    #whatcha의 메인 검색 페이지
    driver.get(url)
    elem = driver.find_element_by_name('search') # 왓챠의 메인 search name
    elem.send_keys(title) #search block에 키워드 입력
    elem.send_keys(Keys.RETURN) #엔터 입력

    #검색된 페이지에서 title에 해당하는 항목 선택
    a = driver.find_elements_by_xpath(xpath_watcha) #anchor xpath 객체 생성
    content_url = a[0].get_attribute('href')
    driver.get(content_url) #해당 객체에서 href 경로로 이동

    #title 세부 정보 페이지
    req = driver.page_source
    return BeautifulSoup(req, 'html.parser'), content_url #html 넘기기

def get_score(page):
    s = page.select_one('div.css-ag7vr6-ContentRatings.e1sxs7wr16').text #별점 div 특정
    score = ''
    for i in range(len(s)):
        if s[i] == '.':
            score += s[i-1:i+2]
    return score

def get_actorlist(page):
    actor_list = page.select('a.css-oeirkd-LinkSelf.eoohahh1')
    actor = []
    for i in range(1,len(actor_list)):
        if i == 4:
            break
        try:
            tmp = actor_list[i].text
            actor.append(tmp[0:len(tmp)-2]) # 배우
        except:
            break
    return actor

def get_summary(page):
    summary_text = page.select_one('div.css-ttw9sz-Text.e13o4ips1').text #영화내용
    summary = ''
    blank = False
    for i in range(len(summary_text)):
        if summary_text[i] == ' ' and blank:
            continue
        else :
            summary += summary_text[i]
        if summary_text[i] == ' ':
            blank = True
        else :
            blank = False
    return summary

chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
chrome_option.add_argument('headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('lang=ko_KR') #selenium 에서 gui 작동 안하게 headless 옵션 달아줌
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
driver.implicitly_wait(3) #랜더링 완료 시간 대기

site_name = 'watcha'
doc_id = 0
content_url = ''
category = 'movie'
title = '아이언맨 3' #항목 생성하려는 대상 이름
actor = ''
summary = ''
score = ''
review = ''

url = 'https://watcha.com/ko-KR' #crawling 하려는 사이트 url
xpath_watcha = '//*[@id="root"]/div/div[1]/section/section/section[2]/div[2]/div[1]/div/div/div/ul/li[@*]/a[@title="'+title+'"]' #watcha 사이트의 세부 정보 링크 xpath, xpath 문법 중요

page, content_url = get_html(url, title, xpath_watcha) #html 과 url링크 가져옴
score = get_score(page) #별점
actor = get_actorlist(page) # 배우
summary = get_summary(page) # 내용

print('****************************************')
print('사이트명 : ', site_name)
print('doc Id : ', doc_id)
print('url : ',content_url)
print('category : ', category)
print('title : ', title)
print('actor : ', actor)
print('summary : ', summary)
print('score : ', score)

json_file = OrderedDict()
json_file["site_name"] = site_name
json_file["doc_id"] = doc_id
json_file["url"] = content_url
json_file["category"] = category
json_file["data"] = {'title' : title, 'actor' : actor, 'summary' : summary}
json_file["score"] = score

with open('./data/movie/'+site_name+'_'+title+'.json', 'w', encoding='utf-8') as make_file:
    json.dump(json_file, make_file, ensure_ascii=False, indent="\t")
