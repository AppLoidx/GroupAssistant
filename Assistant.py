from associates.associator import Associate
from enums.command_enum import CommandEnum
from enums.mode_enum import ModeEnum
from enums.message_enum import MessageEnum
from enums.requests_enum import RequestEnum
from group_persons import *
from group_queue.queue import Queue
from schedule.schedule_from_file import ScheduleFromFile
from editor.json_file import JSONFile
from questions.get_question import GetQuestionJava


class Assistant:

    def __init__(self, vkid, isu_id, group_file_name):

        self.group_file_name = group_file_name
        self.vkid = vkid
        self.isu_id = isu_id
        self.persons = get_group_persons()
        self.from_group_possible_commands = [CommandEnum.get_history,
                                             CommandEnum.person_passed,
                                             CommandEnum.get_queue,
                                             CommandEnum.now_mode,
                                             CommandEnum.new_queue,
                                             CommandEnum.schedule]

        self.now_mode = ModeEnum.DEFAULT
        self.last_mode = ModeEnum.DEFAULT
        self.queue = Queue()
        self.last_question = None
        self.last_command = None
        self.last_ask_yes_no_ans = None  # После завершения всегда присваивать None
        self.last_get_number_ans = None  # После завершения всегда присваивать None
        self.future_def = self.default_def  # функция которая исполнится первым
        self.not_readable_commands = []
        self.schedule = ScheduleFromFile()
        self.java_question = GetQuestionJava()

    def default_def(self):
        pass

    @staticmethod
    def identify_mode_change(command):
        if list(command)[0] == "/":
            for mode in ModeEnum:
                if command[1::] in mode.value:
                    return [True, mode]
        return [False, ModeEnum.UNKNOWN]

    def change_mode(self, to_mode):
        """ Изменяет мод, для следующего поступающего потока команд"""
        self.last_mode = self.now_mode
        self.now_mode = to_mode

    def command(self, command, from_id=None) -> any:
        """

        Сюда вводятся все команды пользователя. Команды разделены на моды,
        чтобы не было конфликтов среди имен и лишних взаимодействий с ботом.

        :param command: команда вводимая пользователем или "супер"-команда
        :param from_id: Если None, то сообщение из группы, если есть значение, то личное
        :return: вывод (ответ бота)
        """
        print(command)

        if command == "":
            command = "unknown"
        if command is None:
            print("Command is None")

        # Обработка нечитаемых событий
        if command in self.not_readable_commands:
            return

        # Обработка особых событий
        if len(command) > 2:
            if command[0:2:] == "$$":
                if command[2:6] == "swap":

                    if self.last_ask_yes_no_ans is None:
                        # TODO mod change()
                        self.change_mode(ModeEnum.YES_NO_ASK)
                        self.last_command = command
                        return "Вы хотите поменяться местами с номером ИСУ " + command.split()[1] + "? (" \
                               + JSONFile.get_persons(self.group_file_name)[command.split()[1]]['name'] + ")"
                    else:
                        if self.last_ask_yes_no_ans:
                            if self.queue.exist_check():
                                command = command.split()
                                self.queue.swap(command[1], command[2])
                                self.queue.write_queue_on_file()
                                self.change_mode(ModeEnum.DEFAULT)
                                self.last_ask_yes_no_ans = None
                                return "Заявка принята!"
                            else:
                                return "Очереди нет"
                        else:
                            return "Вы отклонили запрос!"

        command = self.set_command(command, self.now_mode)

        self.future_def()
        # Command identify

        change_mode = self.identify_mode_change(command['text'])
        if change_mode[0]:
            self.change_mode(change_mode[1])
            print(self.now_mode, "=now mode")
            return "Режим успешно изменён!\n Текущий режим: " + self.now_mode.value[0]

        if from_id is None:
            not_possible_command = True
            for cmd in self.from_group_possible_commands:
                if command['text'] in cmd.value or command['text'].split()[0] in cmd.value:
                    command["command_enum"] = cmd
                    command["message_enum"] = MessageEnum.send_to_group
                    not_possible_command = False
            if not_possible_command:
                return "Недопустимая команда для группы!"
        else:
            command['from_id'] = from_id
            for cmd in CommandEnum:
                if command['text'] in cmd.value:
                    command["command_enum"] = cmd
                    command["message_enum"] = MessageEnum.send_to_person

        command_type = command['command_enum']

        # Вывод текущего мода
        if command_type == CommandEnum.now_mode:
            return self.now_mode.value[0]

        if self.now_mode == ModeEnum.YES_NO_ASK:
            if command['text'].upper() in ["Y", "YES", "ДА"]:
                self.now_mode = self.last_mode
                self.last_ask_yes_no_ans = True

            elif command['text'].upper() in ["NO", "N", "НЕТ"]:
                self.now_mode = self.last_mode
                self.last_ask_yes_no_ans = False

            return self.command(self.last_command)

        if self.now_mode == ModeEnum.GET_NUMBER:
            try:
                self.last_get_number_ans = int(command['text'])

            except ValueError:
                return "Введите цифру!"

            self.now_mode = self.last_mode
            return self.command(self.last_command, from_id)

        #
        #              MAIN COMMANDS
        #

        # QUESTION MODE
        if self.now_mode == ModeEnum.QUESTION:
            if command['text'] in CommandEnum.get_java_question.value:
                return self.java_question.get_question()[1]
            elif command['text'] in CommandEnum.get_java_answer.value:
                return self.java_question.last_answer
            else:
                return "Не могу распознать вашу команду, простите."
        # DEFAULT MODE
        if self.now_mode == ModeEnum.DEFAULT:

            # schedule

            if len(command['text'].split()) > 1:
                if command['text'].split()[0] in CommandEnum.schedule.value:
                    if command['text'].split()[1] == "завтра":
                        return self.schedule.get_schedule(1)
                    if len(command['text'].split()) > 2:
                        if command['text'].split()[1] == "на" and command['text'].split()[2] == "завтра":
                            return self.schedule.get_schedule(1)
                    try:
                        return self.schedule.get_schedule(int(command['text'].split()[1]))
                    except TypeError:
                        return "Неверный формат[TP]! Расписание <через k: int дней>/<на завтра>"
                    except ValueError:
                        return "Неверный формат[VE]! Расписание <через k: int дней>/<на завтра>"
            if command['text'] in CommandEnum.schedule.value:
                return self.schedule.get_schedule()

            # journal link

            if len(command['text'].split()) > 1:
                if command['text'].split()[0] in CommandEnum.get_journal_link.value:
                    data = JSONFile.read_json("links.json")

                    associate = Associate.get_associate(command['text'].split()[1])
                    if isinstance(associate, Exception):
                        return "У меня тут что-то пошло не так... Вы все правильно ввели?"
                    if associate is None:
                        return "Не нашла такого журнала в своей базе данных..."
                    return data['journals'][associate]

        # REQUEST MODE
        if self.now_mode == ModeEnum.REQUEST:
            if command['text'] in RequestEnum.SWAP.value:
                if self.last_get_number_ans is None:
                    self.change_mode(ModeEnum.GET_NUMBER)
                    self.last_command = command['text']
                    return "Введите номер ИСУ с которым хотите поменяться:"
                else:

                    JSONFile.add_request("swap", f"{self.isu_id} {self.last_get_number_ans}")
                    self.last_get_number_ans = None
                    self.now_mode = self.last_mode
                    return "Успешно!"

        print(command_type)

        # QUEUE MODE
        if self.now_mode == ModeEnum.QUEUE:

            if command_type == CommandEnum.new_queue:
                if self.queue.exist_check():
                    return "Очередь уже существует. Если вы хотите удалить его, то сделайте заявку."
                else:
                    self.queue.new_queue()
                    self.queue.write_queue_on_file()

                    return "Очередь создана!"

            # Функции не изменяющие очередь
            elif command_type == CommandEnum.get_history:
                print("history")
                result = ""
                for i in self.queue.history.get_history():
                    result += i + "\n"

                return result

            elif command_type == CommandEnum.get_queue:
                if self.queue.exist_check():
                    self.queue.update_queue()

                    result = ""
                    for person in self.queue.get_queue():
                        result += f"{person.get_name()} id:{person.get_id()}"
                        if person.get_passed():
                            result += " [прошел]"
                        else:
                            result += " [ожидает]"
                        result += "\n"

                    return result
                else:
                    return "Очереди нет"

            elif command_type == CommandEnum.get_last_person_in_queue:
                if self.queue.exist_check():
                    self.queue.update_queue()

                    return self.queue.get_last_person_in_queue().get_name()
                else:
                    return "Очереди нет"

            elif command_type == CommandEnum.get_current_person_in_queue:
                if self.queue.exist_check():
                    self.queue.update_queue()

                    return self.queue.get_current_person_in_queue().get_name()
                else:
                    return "Очереди нет"

            elif command_type == CommandEnum.get_next_person_in_queue:
                if self.queue.exist_check():
                    self.queue.update_queue()

                    return self.queue.get_next_person_in_queue().get_name()
                else:
                    return "Очереди нет"

            # Функции меняющие очерердь

            elif command_type == CommandEnum.person_passed:
                if self.queue.exist_check():
                    self.queue.update_queue()

                    if from_id is None:
                        self.queue.person_passed()
                        self.queue.write_queue_on_file()
                        return f"{self.queue.get_last_person_in_queue().get_name()} прошел"

                    else:
                        return "Напишите пожалуйста в группу!"
                else:
                    return "Очереди нет"

        return "Не распознанная команда!"

    # TODO: Rewrite to class
    @staticmethod
    def set_command(command, now_mode):

        return {"text": command,
                "message_enum": MessageEnum.unknown,
                "command_enum": CommandEnum.unknown,
                "mode": now_mode,
                "from_id": None}
