import json
import requests

default_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=430156241533f1d058c603178cc3ca0e&curPage='
index = 1
f = open('data/movie/input/movie_list_'+ str(index) +'.txt', mode='wt', encoding='utf-8')
for i in range(1,1001):#7054
    url = default_url + str(i)
    response = requests.get(url)
    json_dummy = json.loads(response.text)
    movie_list = json_dummy['movieListResult']['movieList']
    for n in movie_list:
        id = n['movieCd']
        title = n['movieNm']
        year = n['openDt']
        f.write('%d|%s|%s|%s\n'%(i,id,title,year))
    if i%100 == 0:
        f.close()
        print('file'+str(index)+' complete!')
        index += 1
        f = open('data/movie/input/movie_list_'+ str(index) +'.txt', mode='wt', encoding='utf-8')
f.close()
