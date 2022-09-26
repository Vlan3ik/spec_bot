import requests
URL = "http://smolapo.ru/sites/default/files/Studentam/2022-2023/rasp%2022-23-1.xlsx"
response = requests.get(URL)
open("rasp%2022-23-1.xls", "wb").write(response.content)