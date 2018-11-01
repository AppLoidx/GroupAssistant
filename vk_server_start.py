from Assistant import Assistant
from editor.editor import Edit
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from config import group_vk_api_token
from editor.json_file import JSONFile
from parser_m.parser import Parser


def set_persons(filename="groupList.json"):
    data = JSONFile.read_json(filename)
    res = {}
    for info in data['Persons']:
        res[data["Persons"][info]['vkid']] = Assistant(data["Persons"][info]['vkid'], info)

    return res


parser = Parser()

token = group_vk_api_token  # access_token
vk = vk_api.VkApi(token=token)
vk_s = vk.get_api()

longpoll = VkBotLongPoll(vk, 173296780)

ids = set_persons()


def start():
    # Слушаем сервер
    for event in longpoll.listen():

        do_requests_list()
        # Новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:

            if str(event.object.from_id) not in ids:
                ids[str(event.object.from_id)] = Assistant(event.object.from_id,
                                                           get_id_by_vkid(str(event.object.from_id)))

            print('Новое сообщение:')

            if event.group_id:
                pass
            print('Текст: ', event.object.text, end="\n")

            """
            vk_s.messages.send(peer_id=event.object.peer_id,
            message=None)
            """
            if event.object.id == 0:
                vk_s.messages.send(peer_id=event.object.peer_id,
                                   message=ids[str(event.object.from_id)].command(
                                       Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" ")))
            else:
                vk_s.messages.send(peer_id=event.object.peer_id,
                                   message=ids[str(event.object.from_id)].command(
                                       Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" "),
                                       event.object.from_id))


def do_requests_list(filename="request_list.json"):
    data = JSONFile.read_json(filename)
    for request_type in data["request"]:
        index = 0
        max_value_index = len(data['request'][request_type])
        while index < max_value_index:
            swap_c = data['request'][request_type][index].split()
            cmd = "$$swap " + swap_c[0] + " " + swap_c[1]

            ids[get_vkid_by_id(swap_c[0])].command(cmd)

            del data['request'][request_type][index]
            max_value_index -= 1

            index += 1

            if index == max_value_index:
                break

    JSONFile.set_json_data(data, filename)


def get_vkid_by_id(id):
    data = JSONFile.read_json("groupList.json")
    return data["Persons"][id]['vkid']


def get_id_by_vkid(vkid):
    data = JSONFile.read_json("groupList.json")
    for id in data['Persons']:
        if data["Persons"][id]['vkid'] == vkid:
            return id


print("Server runned...")


def mainloop(exceptions=0):
    if exceptions > 9:
        vk_s.messages.send(peer_id=255396611,
                           message="Произошло больше 9 ошибок. Отключаю сервер...")
        return

    try:
        start()
    except Exception:
        vk_s.messages.send(peer_id=255396611,
                           message="Произошла ошибка! Перезапускаюсь!")
        mainloop(exceptions + 1)


mainloop()