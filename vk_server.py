import vk_api.vk_api
from Assistant import Assistant

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from config import group_vk_api_token
from config import admin_vk_id

from editor.json_file import JSONFile
from enums.mode_enum import ModeEnum
from parser_m.parser import Parser

from messenger.messenger import Messenger
from spam import Spam


class VkServer:

    def __init__(self, server_name, group_file_name, group_id, api_token):
        self.server_name = server_name
        self.group_file_name = group_file_name
        self.parser = Parser()

        print(f"[{server_name}] connection to vk API...")

        self.vk = vk_api.VkApi(token=api_token)
        self.vk_s = self.vk.get_api()

        self.longpoll = VkBotLongPoll(self.vk, group_id, wait=25)

        self.ids = self._set_persons(group_file_name)

        self.messenger = Messenger(self.vk_s, self.ids)

        self.spam = Spam(self.vk_s, self.ids, self.group_file_name)

        print("Server " + self.server_name + " working...")

    def _set_persons(self, filename):
        data = JSONFile.read_json(filename)
        res = {}
        for info in data['Persons']:
            res[data["Persons"][info]['vkid']] = Assistant(self.vk_s, data["Persons"][info]['vkid'], info,
                                                           self.group_file_name)

        return res

    def start(self):
        # Слушаем сервер
        for event in self.longpoll.listen():
            self.do_requests_list()
            # Новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:

                if str(event.object.from_id) not in self.ids:
                    self.ids[str(event.object.from_id)] = Assistant(self.vk_s, event.object.from_id,
                                                                    JSONFile.get_id_by_vkid(str(event.object.from_id),
                                                                                            self.group_file_name),
                                                                    self.group_file_name, True)

                if event.group_id:
                    pass

                """
                vk_s.messages.send(peer_id=event.object.peer_id,
                message=None)
                """
                if True:  # event.object.from_id == admin_vk_id:
                    if event.object.id == 0:
                        self.messenger.send_message(event.object.from_id, "Сообщения в группе запрещены. "
                                                                          "Пожалуйста, пишите в личные сообщения)))")
                    else:

                        self.messenger.send_message_by_event(event, from_id=event.object.from_id)

                else:
                    self.messenger.send_message_by_event(event, str(JSONFile.get_name_by_vkid(event.object.from_id,
                                                                                              self.group_file_name)) +
                                                         ", сейчас я нахожусь в тестовом режиме!")

    def do_requests_list(self, filename="request_list.json"):
        data = JSONFile.read_json(filename)
        for request_type in data["request"]:
            index = 0
            max_value_index = len(data['request'][request_type])
            if request_type == "swap":
                while index < max_value_index:
                    swap_c = data['request'][request_type][index].split()
                    cmd = "$$swap " + swap_c[0] + " " + swap_c[1]

                    self.ids[JSONFile.get_vkid_by_id(swap_c[1], self.group_file_name)].command(cmd)

                    del data['request'][request_type][index]
                    max_value_index -= 1

                    index += 1

                    if index == max_value_index:
                        break
            elif request_type == "send2all":
                if len(data['request']['send2all']) > 0:
                    self.spam.send_spam(data['request']['send2all'])
                    del data['request']['send2all'][0]

        JSONFile.set_json_data(data, filename)

    def mainloop(self, exceptions=0):
        if exceptions > 9:
            self.vk_s.messages.send(peer_id=admin_vk_id,
                                    message="Произошло больше 9 ошибок. Отключаю сервер...")
            return

        try:
            self.start()

        except Exception as e:
            self.vk_s.messages.send(peer_id=admin_vk_id,
                                    message="Произошла ошибка! Перезапускаюсь! " + e.__str__())
            self.mainloop(exceptions + 1)

    def get_server_name(self):
        return self.server_name
