import json
import requests
import time

default_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=430156241533f1d058c603178cc3ca0e&curPage='
index = 1
f = open('data/movie_list_'+ str(index) +'.txt', mode='wt', encoding='utf-8')
for i in range(1,7054):#7054 , 1 ~ 1000
    url = default_url + str(i)
    response = requests.get(url)
    json_dummy = json.loads(response.text)
    movie_list = json_dummy['movieListResult']['movieList']
    for n in movie_list:
        id = n['movieCd'] # 영화 고유값
        title = n['movieNm'] # 영화 명
        contry = n['repNationNm'] # 영화 제작 국가
        open_year = n['openDt'] # 개봉년월일
        start_year = n['prdtYear'] #제작년월일
        f.write('%d|%s|%s|%s|%s|%s\n'%(i,id,title,contry,open_year,start_year))
    if i%100 == 0:
        f.close()
        print('file'+str(index)+' complete!')
        time.sleep(5)
        index += 1
        f = open('data/movie/input/movie_list_'+ str(index) +'.txt', mode='wt', encoding='utf-8')
f.close()
