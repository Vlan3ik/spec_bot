import requests
from lxml import html
import urllib.request
import datetime
now = datetime.datetime.now()



req = requests.get("http://smolapo.ru/node/168")
print(req.status_code)
if req.status_code == 200:
    tree = html.fromstring(req.text)
    hrefs = tree.xpath('/html/body/div[2]/div/div[5]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/form/div/fieldset[3]/div/div/ol/li[2]/a')
    hrefs2 = tree.xpath('/html/body/div[2]/div/div[5]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/form/div/fieldset[3]/div/div/ol/li[5]/a')
    raspisanie = hrefs[0].attrib['href']
    izmineniya = hrefs2[0].attrib['href']
    print(f"Расписание {raspisanie}\nИзминения {izmineniya}")
    urllib.request.urlretrieve(f"http://smolapo.ru{raspisanie}","raspisanie.xlsx")
    urllib.request.urlretrieve(f"http://smolapo.ru{izmineniya}","izm.docx")
