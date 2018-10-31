from Assistant import Assistant
from editor.editor import Edit
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from config import group_vk_api_token
from parser_m.parser import Parser

parser = Parser()

token = group_vk_api_token  # access_token
vk = vk_api.VkApi(token=token)
vk_s = vk.get_api()

longpoll = VkBotLongPoll(vk, 173296780)

ids = {}


def start():
    # Слушаем сервер
    for event in longpoll.listen():

        do_requests_list()
        # Новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.object.from_id not in ids:
                ids[str(event.object.from_id)] = Assistant(event.object.from_id, get_id_by_vkid(str(event.object.from_id)))

            print('Новое сообщение:')

            if event.group_id:
                pass
            print('Текст: ', event.object.text, end="\n")

            """
            vk_s.messages.send(peer_id=event.object.peer_id,
            message=None)
            """
            vk_s.messages.send(peer_id=event.object.peer_id,
                               message=ids[str(event.object.from_id)].command(
                                   Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" ")))


def do_requests_list():
    f = open("requests_list.txt", "r", encoding="UTF-8")
    data = f.read().split("\n")
    for req in data:
        if req == "":
            continue
        req = req.split()
        if req[0] == "queue":
            if req[1] == "swap":
                vkid = get_vkid_by_id(req[2])
                if vkid is not None:
                    #try:
                    print("$$swap "+str(req[2]) + " " + str(req[3]))
                    return ids[vkid].command("$$swap "+str(req[2]) + " " + str(req[3]))
                    #except KeyError:
                    #print("Key Error")


def get_vkid_by_id(id):
    f = open("groupList.txt", "r", encoding="UTF-8")
    data = f.read().split("\n")
    for p in data:
        p = p.split()
        if len(p) > 3:
            if p[0] == id:
                return p[3]
    return None


def get_id_by_vkid(vkid):
    f = open("groupList.txt", "r", encoding="UTF-8")
    data = f.read().split("\n")
    for p in data:
        p = p.split()
        if len(p) > 3:
            if p[3] == vkid:
                return p[0]
    return None

print("Server runned...")
start()