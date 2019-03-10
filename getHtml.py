import requests

def get_html(url):
    output = ""
    response = requests.get(url)
    if response.status_code == 200:
        output = response.text
    return output    


url = "http://www.statiz.co.kr/player.php?opt=10&name=%EC%B5%9C%EC%A0%95&birth=1987-02-28"
text = get_html(url)
f = open('output/sample.txt',mode='wt',encoding='utf-8')
f.write(text)
f.close()
