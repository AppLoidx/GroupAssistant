import vk_api.vk_api
from Assistant import Assistant
from editor.editor import Edit

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from config import group_vk_api_token
from config import admin_vk_id

from editor.json_file import JSONFile
from parser_m.parser import Parser


class VkServer:

    def __init__(self, server_name, group_file_name, group_id):
        self.server_name = server_name
        self.group_file_name = group_file_name
        self.parser = Parser()

        print(f"[{server_name}] connection to vk API...")
        self.vk = vk_api.VkApi(token=group_vk_api_token)
        self.vk_s = self.vk.get_api()

        self.longpoll = VkBotLongPoll(self.vk, group_id)

        self.ids = self._set_persons(group_file_name)

        print("Server " + self.server_name + " working...")

    def _set_persons(self, filename):
        data = JSONFile.read_json(filename)
        res = {}
        for info in data['Persons']:
            res[data["Persons"][info]['vkid']] = Assistant(data["Persons"][info]['vkid'], info, self.group_file_name)

        return res

    def start(self):
        # Слушаем сервер
        for event in self.longpoll.listen():
            self.do_requests_list()
            # Новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:

                if str(event.object.from_id) not in self.ids:
                    self.ids[str(event.object.from_id)] = Assistant(event.object.from_id,
                                                                    JSONFile.get_id_by_vkid(str(event.object.from_id),
                                                                                            self.group_file_name))

                print('Новое сообщение:')

                if event.group_id:
                    pass
                print('Текст: ', event.object.text, end="\n")

                """
                vk_s.messages.send(peer_id=event.object.peer_id,
                message=None)
                """
                if event.object.id == 0:
                    self.vk_s.messages.send(peer_id=event.object.peer_id,
                                            message=self.ids[str(event.object.from_id)].command(
                                                Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" ")))
                else:
                    self.vk_s.messages.send(peer_id=event.object.peer_id,
                                            message=self.ids[str(event.object.from_id)].command(
                                                Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" "),
                                                event.object.from_id))

    def do_requests_list(self, filename="request_list.json"):
        data = JSONFile.read_json(filename)
        for request_type in data["request"]:
            index = 0
            max_value_index = len(data['request'][request_type])
            while index < max_value_index:
                swap_c = data['request'][request_type][index].split()
                cmd = "$$swap " + swap_c[0] + " " + swap_c[1]

                self.ids[JSONFile.get_vkid_by_id(swap_c[1], self.group_file_name)].command(cmd)

                del data['request'][request_type][index]
                max_value_index -= 1

                index += 1

                if index == max_value_index:
                    break

        JSONFile.set_json_data(data, filename)

    def mainloop(self, exceptions=0):
        if exceptions > 9:
            self.vk_s.messages.send(peer_id=admin_vk_id,
                                    message="Произошло больше 9 ошибок. Отключаю сервер...")
            return

        try:
            self.start()

        except Exception:
            self.vk_s.messages.send(peer_id=admin_vk_id,
                                    message="Произошла ошибка! Перезапускаюсь!")
            self.mainloop(exceptions + 1)

    def get_server_name(self):
        return self.server_name


""" Notes

requests.exceptions.ConnectionError
"""
