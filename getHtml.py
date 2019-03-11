import csv
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
f = open('output/sample.csv',mode='wt',newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(['날짜','상대팀','이닝','투수','타자','볼카운트','결과','이전상황','이후상황','LEV','REa','WPs','WPe','WPa'])


for n in range(0,len(data),14):
    csv_writer.writerow([data[n].get_text(),data[n+1].get_text(),data[n+2].get_text(),data[n+3].get_text(),data[n+4].get_text(),data[n+5].get_text().replace('-','S - ')+'B',data[n+6].get_text(),data[n+7].get_text(),data[n+8].get_text(),data[n+9].get_text(),data[n+10].get_text(),data[n+11].get_text(),data[n+12].get_text(),data[n+13].get_text()])
    
f.close()

