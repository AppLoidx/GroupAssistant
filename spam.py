from editor.json_file import JSONFile
from messenger.messenger import Messenger


class Spam:

    def __init__(self, vk_api, ids, group_file_name):
        self.ids = ids
        self.messenger = Messenger(vk_api, ids)
        self.group_file_name = group_file_name

    def send_spam(self, msg: str, exceptions_id: list=[], exceptions_vkid=[]):
        for vkid in self.ids:
            if vkid in exceptions_vkid:
                pass
            elif JSONFile.get_id_by_vkid(vkid, self.group_file_name) in exceptions_id:
                pass
            elif vkid is None:
                pass
            elif not JSONFile.read_json(self.group_file_name)["Persons"][self.ids[vkid].isu_id]['settings']['4all_msg']:
                pass
            else:
                self.messenger.send_message(vkid, msg)

    def test_send(self, msg):
        pass