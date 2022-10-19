import vk_api
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import threading
import requests
import requests
from lxml import html
import urllib.request
import json
from config import config , days , check
from datetime import datetime





class Bot_Main:

    def __init__(self) -> None:
        self.session = requests.Session()
        self.vk_session = vk_api.VkApi(token=config["token"])
        self.vk = self.vk_session.get_api()
        self.upload = VkUpload(self.vk_session)
        self.longpoll = VkBotLongPoll(self.vk_session, config["id"])

    def download_raspisanie():
        req = requests.get("http://smolapo.ru/node/168")
        print(req.status_code)
        if req.status_code == 200:
            try:
                tree = html.fromstring(req.text)
                hrefs2 = tree.xpath('/html/body/div[2]/div/div[5]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/form/div/fieldset[3]/div/div/ol/li[5]/a')
                izmineniya = hrefs2[0].attrib['href']
                urllib.request.urlretrieve(f"http://smolapo.ru{izmineniya}","izm.docx")
                return True
            except Exception as err:
                return err
        else:
            return req.status_code
    
    def Sender(self,id,text,if_rasp , peer):
        if if_rasp == True:
            result = json.loads(requests.post(self.vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],files={'file': open('izm.docx', 'rb')}).text)
            jsonAnswer = self.vk.docs.save(file=result['file'], title='izm.docx', tags=[])
            self.vk.messages.send(
                peer_id= peer,
                random_id=get_random_id(),
                message=f"Держи расписание зайка\n\n{Bot_Main.Get_Raspisanie()}\n\nИзминения" ,
                attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
                )
        else:
            self.vk.messages.send(
                user_id=id ,
                random_id=get_random_id(),
                message=text )
    
    def Get_Raspisanie():
        from datetime import datetime
        date1 = datetime.now()
        date2 = datetime(day=1, month=9, year=2022)
        timedelta = (date1 - date2)// 7
        q = 0
        w = ""
        print(timedelta.days )
        if (timedelta.days % 2) != 0:
            q = 1
            w = "Числитель"
        else:
            q = 2
            w = "Знаменатель"
        day = datetime.isoweekday(date1)
        rasp = days[str(day)]
        rasp2 = days[str(day + 1)]
        try:
            rasp = rasp.replace("chek" , check[f"{day}{q}"] )
        except:
            pass
        try:
            rasp2 = rasp2.replace("chek" , check[f"{int(day)+1}{q}"] )
        except:
            pass

        text = f"{w} / {timedelta.days } Неделя\n\nСЕГОДНЯ\n{rasp}\n\nЗАВТРА\n{rasp2}"

        return text


    def Processing_Message(self,event):
        message = event.obj['message']
        peer = message['peer_id']
        text = message['text']
        if text.lower() == "расписание":
            download = Bot_Main.download_raspisanie()
            if download == True:

                Bot_Main.Sender(self,event.obj.from_id ,f"" , True , peer)
            elif type(download) is str:
                Bot_Main.Sender(self,event.obj.from_id ,f"Опять тупая ошибка в парсе\nОшибка:\n{download}" , False , peer)
            else:
                Bot_Main.Sender(self,event.obj.from_id ,f"Сайт не даёт парсить\nКод ошибки {download}", False , peer)
            

    def Start_Bot(self):
        while True:
            try:
                print("start")
                for event in self.longpoll.listen():
                    print(event.type)
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        threading.Thread(target=Bot_Main.Processing_Message, args=(self,event)).start()
            except Exception:
                pass


if __name__ == '__main__':
    bot = Bot_Main()
    bot.Start_Bot()