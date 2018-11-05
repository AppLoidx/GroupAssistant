from editor.editor import Edit
from editor.json_file import JSONFile
from vk_api.vk_api import ApiError

from enums.mode_enum import ModeEnum


class Messenger:
    def __init__(self, vk_api, ids):
        self.vk = vk_api
        self.ids = ids

    def send_message_by_event(self, event, msg=None, keyboard=None, from_id=None):

        if msg is None:
            msg = self.ids[str(event.object.from_id)].command(
                Edit.clean_str_from_symbol(event.object.text, "[", "]").strip(" "), from_id)

        if msg.strip("\n") == "" or msg is None:
            msg = "(Пусто)"

        assistant_mode = self.ids[str(event.object.from_id)].get_mode()

        if keyboard is None:
            keyboard = None
            if assistant_mode == (ModeEnum.GET_STRING or ModeEnum.GET_NUMBER):
                keyboard = "none.json"
            elif assistant_mode == ModeEnum.YES_NO_ASK:
                keyboard = "yes_no_ask.json"
            elif assistant_mode == ModeEnum.DEFAULT:
                keyboard = "default.json"
            elif assistant_mode == ModeEnum.QUEUE:
                keyboard = "queue.json"
            elif assistant_mode == ModeEnum.QUESTION:
                keyboard = "question.json"
            elif assistant_mode == ModeEnum.REQUEST:
                keyboard = "request.json"

        if from_id is None:
            if keyboard is not None:
                self.vk.messages.send(peer_id=event.object.peer_id,
                                      message=msg,
                                      keyboard=JSONFile.read_keyboard(keyboard))
            else:
                self.vk.messages.send(peer_id=event.object.peer_id,
                                      message=msg)
        else:
            if keyboard is not None:
                self.vk.messages.send(peer_id=event.object.peer_id,
                                      message=msg,
                                      keyboard=JSONFile.read_keyboard(keyboard))
            else:
                self.vk.messages.send(peer_id=event.object.peer_id,
                                      message=msg)

    def send_message(self, peer_id, msg):
        if msg == "":
            msg = "None"
        print("send to " + str(peer_id))
        try:
            self.vk.messages.send(user_id=int(peer_id), message=msg, keyboard=open("keyboards/none.json", "r").read())
        except ApiError:
            print("Ошибка доступа!")