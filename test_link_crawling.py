import pytest
from selenium import webdriver
import link_crawling
import json

#pytest --site 0,1,2,3 test_link_crawling.py

@pytest.fixture(scope = 'module')
def site_index(pytestconfig):
    val = pytestconfig.getoption("site")
    return int(val)

@pytest.fixture(scope = 'module')
def browser():
    chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
    #chrome_option.add_argument('headless')
    chrome_option.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
    driver.implicitly_wait(3) #랜더링 완료 시간 대기
    yield driver
    driver.close()

@pytest.fixture(scope = 'module')
def site(site_index):
    site_list = link_crawling.read_site_list()
    return site_list[site_index]

@pytest.fixture(scope = 'module')
def movie():
    m_l = ['어벤져스','미국','2012','2012']
    return m_l[1]

@pytest.fixture(scope = 'module')
def result_json(site_index):
    f = open('data/movie/test/엑시트_link.json',mode='r',encoding='utf-8')
    json_result = json.load(f)
    result = json_result['links']
    f.close()
    return result[site_index]

@pytest.fixture(scope = 'module')
def browser_list(browser, site, movie):
    driver = browser
    title = movie[0]
    default_url = site['site_url']
    search_xpath = site['search_xpath']
    link_crawling.search_title(driver,title,default_url,search_xpath)
    return driver

@pytest.fixture(scope = 'module')
def browser_content(browser, site, movie):
    driver = browser
    title = movie[0]
    default_url = site['site_url']
    search_xpath = site['search_xpath']
    link_crawling.search_title(driver,title,default_url,search_xpath)
    contry = movie[1]
    open_year = movie[2]
    start_year = movie[3]
    title_xpath = site['title_xpath']
    check_xpath = site['check_xpath']
    link_crawling.get_url(driver, title, contry, open_year, start_year, title_xpath, check_xpath)
    return driver

def test_remove_blank():
    text = 'abcd efgh'
    result = link_crawling.remove_blank(text)
    assert result == 'abcdefgh'

def test_init():
    driver = link_crawling.init()
    assert driver #안됐을 때 케이스에 대한 고려

def test_read_site_list(site_index):
    site_list = link_crawling.read_site_list()
    test = ['watcha','naver_movie','daum_movie','maxmovie']
    assert test[site_index] == site_list[site_index]['site_name']

def test_read_movie_list():
    movie_list = link_crawling.read_movie_list()
    assert len(movie_list[0]) == 4

def test_search_title(browser, site, movie):
    driver = browser
    title = movie[0]
    default_url = site['site_url']
    search_xpath = site['search_xpath']
    link_crawling.search_title(driver,title,default_url,search_xpath)
    assert 1

def test_get_url(browser_list, site, movie):
    driver = browser_list
    title = movie[0]
    contry = movie[1]
    open_year = movie[2]
    start_year = movie[3]
    title_xpath = site['title_xpath']
    check_xpath = site['check_xpath']
    content_url = link_crawling.get_url(driver, title, contry, open_year, start_year, title_xpath, check_xpath)
    assert 1

def test_get_score(browser_content, site, result_json):
    driver = browser_content
    score_xpath = site['score_xpath']
    score = link_crawling.get_score(driver, score_xpath)
    scale = site['scale_type']
    score = link_crawling.score_scaling(score, scale)
    expect_rating = result_json['rating']
    assert score == expect_rating
