from bs4 import BeautifulSoup
import requests

def get_html(url):
    output = ""
    response = requests.get(url)
    if response.status_code == 200:
        output = response.text
    return output    


url = "http://www.statiz.co.kr/player.php?opt=6&sopt=0&name=%EC%B5%9C%EC%A0%95&birth=1987-02-28&re=0&da=1&year=2018&plist=&pdate="
text = get_html(url)
soup = BeautifulSoup(text, 'html.parser')
data = soup.find("table",{"class":"table-striped"}).find_all("td") #가까운 table을 찾고 그 안에 모든 td를 추출, 반환형이 string 아님
f = open('output/sample.txt',mode='wt',encoding='utf-8')
cnt = 0
for n in data: #n 자체에 해당 테그정보까지 담고있음
    cnt += 1    
    f.write("%s    "%n.get_text()) #내용만 추출
    if cnt%14 == 0:
        f.write("\n")
        cnt = 0
f.close()
