from editor.json_file import JSONFile
from enums.mode_enum import ModeEnum


class Manual:

    @staticmethod
    def get_manual(mode: ModeEnum, work_dir="manual/"):

        data = {"command": "Мануал не найден!"}

        if mode == ModeEnum.DEFAULT:
            data = JSONFile.read_json(work_dir+"default.json")
        elif mode == ModeEnum.QUEUE:
            data = JSONFile.read_json(work_dir+"queue.json")
        elif mode == ModeEnum.REQUEST:
            data = JSONFile.read_json(work_dir+"request.json")
        elif mode == ModeEnum.QUESTION:
            data = JSONFile.read_json(work_dir+"question.json")
        elif mode == ModeEnum.SETTINGS:
            data = JSONFile.read_json(work_dir+"settings.json")
        else:
            return "Мануал по данному моду пока не создан, либо редактируется."

        res = ""

        for command in data['commands']:
            res += "[" + str(command) + "]" + " - " + data['commands'][command] + "\n"

        return res
