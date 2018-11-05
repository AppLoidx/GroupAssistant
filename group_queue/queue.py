import os
import random

from editor.json_file import JSONFile
from parser_m.date import Date
from group_queue.person import Person
from group_queue.history import History


class Queue:

    def __init__(self, group_file_name):
        self.group_file_name = group_file_name
        self._queue_list = self._set_group_list()
        self._GROUP_LIST = self._queue_list

        # Номер текущей очереди
        self._queue_value = 0

        # Работа с историей
        self.history = History()

    @staticmethod
    def exist_check(filename="queue.txt"):

        return os.path.isfile(filename)

    def _set_group_list(self):
        """
        Получает список группы из файла groupList.txt или groupListWindow.txt в зависимости от кодировки
        :return: сгенерированный список группы с элементами Person
        """

        data = JSONFile.read_json(self.group_file_name)
        group_list = []

        for person in data["Persons"]:
            group_list.append(Person(person, data["Persons"][person]["name"]))

        return group_list

    def new_queue(self, group_list: list=None) -> None:
        """
        Создание новой очереди, начиная с рандомно выбранного человека
        :param group_list: список группы с классами  Person
        :return: None
        """
        if group_list is None:
            group_list = self._queue_list
        self._queue_list = self._create_queue(random.randint(0, 27), group_list)

        self.history.write("Создана новая очередь")

    def write_queue_on_file(self, queue_list=None):
        if queue_list is None:
            queue_list = self._queue_list

        f = open("queue.txt", "w", encoding="UTF-8")
        for person in queue_list:
            f.write(str(person.get_id()))
            f.write(" ")
            f.write(str(person.get_name()))
            f.write(" ")
            f.write(str(person.get_passed()))
            f.write("\n")
        f.close()

    def update_queue(self, filename="queue.txt"):
        f = open(filename, "r", encoding="UTF-8")
        data = f.read().split("\n")
        new_list = []
        self._queue_value = 0
        for p in data:
            if p == "":
                continue
            p = p.split()
            _NAME = p[1] + " " + p[2]
            _ID = p[0]
            if p[3] == "True":
                self._queue_value += 1
                _PASSED = True
            else:
                _PASSED = False

            new_list.append(Person(_ID, _NAME, _PASSED))

        if len(new_list) == len(self._queue_list):
            self._queue_list = new_list

        f.close()

    @staticmethod
    def _create_queue(start_person_id: int, group_list: list) -> list:
        """
        Создает очередь с человека заданного по индексу
        :param start_person_id: индекс человека с которого начинается очередь
        :param group_list: список людей занимающих очередь
        :return: массив с очередью
        """
        queue = []
        for i in range(len(group_list)):
            index = i + start_person_id - 1

            # При переполнении
            if index >= len(group_list):
                index -= len(group_list)

            queue.append(group_list[index])

        return queue

    def person_passed(self) -> None:
        """
        Вызывается когда кто-то прошел очередь. Инициализирует сдвиг очереди
        :return: None
        """
        try:
            self._queue_list[self._queue_value].set_passed(True)
            self.history.write(f"{self._queue_list[self._queue_value].get_id()}"
                               f" {self._queue_list[self._queue_value].get_name()}"
                               f" прошел очередь в {Date.get_time()}")
            self._queue_value += 1

            # При переполнении
            if self._queue_value == len(self._queue_list):
                self._queue_value -= len(self._queue_list)

        except IndexError:
            for person in self._queue_list:
                person.set_passed(False)
            self._queue_value = 0

    def get_last_person_in_queue(self) -> Person:
        """

        :return: Предыдущий в очереди
        """
        if self._queue_value == 0:
            return Person("0", "None")
        else:
            return self._queue_list[self._queue_value - 1]

    def get_current_person_in_queue(self) -> Person:
        """

        :return: Текущий в очереди
        """
        return self._queue_list[self._queue_value]

    def get_next_person_in_queue(self) -> Person:
        """

        :return: Следующий в очереди
        """
        if self._queue_value == len(self._queue_list) - 1:
            return self._queue_list[0]
        else:
            return self._queue_list[self._queue_value + 1]

    def get_queue(self) -> list:
        """
        Получение списка очереди
        :return: список очереди, элементы которой типа Person
        """
        return self._queue_list

    def get_person_queue_position(self, person_id: str) -> int:
        """
        Возвращает текущую позицию в очереди по номеру в списке
        :param person_id: номер в списке
        :return: номер в очереди. 0 - если не найден в очереди
        """
        pos = 0
        passed_people = 0
        for i in range(len(self._queue_list)):
            if self._queue_list[i].get_id() == person_id:
                pos = i + 1
                break
            elif self._queue_list[i].get_passed():
                passed_people += 1
        return pos - passed_people

    def delete_person(self, person_id: str, filename="queue.txt"):
        """
        Удаление персонажа с очереди
        :param person_id: номер ИСУ
        :return: None
        """
        f = open(filename, "r", encoding="UTF-8")
        data = f.read().split("\n")
        new_list = []
        for p in data:
            if p == "":
                continue
            p = p.split()
            _NAME = p[1] + " " + p[2]
            _ID = p[0]
            if p[3] == "True":
                _PASSED = True
            else:
                _PASSED = False

            if _ID == person_id:
                self.history.write(_NAME + " был удален из очереди в " + str(Date.get_time()))
            else:
                new_list.append(Person(_ID, _NAME, _PASSED))

        self._queue_list = new_list

        f.close()

        self.write_queue_on_file()

    def add_person(self, person_id: str, position: int=-1):

        new_queue_list = []

        if position == -1:
            for person in self._GROUP_LIST:
                if str(person.get_id()) == person_id:
                    self._queue_list.append(person)

                    self.history.write(f"В конец очереди добавлен {person.get_name()} в {Date.get_time()}")

        elif position == len(self._queue_list) + 1:
            for person in self._GROUP_LIST:
                if person.get_id() == person_id:
                    self._queue_list.append(person)
                    self.history.write(f"В позицию {position}"
                                       f" добавлен {person.get_name()} в"
                                       f" {Date.get_time()}")

        else:
            for i in range(len(self._queue_list)):
                if i + 1 == position:
                    for person in self._GROUP_LIST:
                        if person.get_id() == person_id:
                            new_queue_list.append(person)
                            self.history.write(f"В позицию {position}"
                                               f" добавлен {person.get_name()} в"
                                               f" {Date.get_time()}")

                new_queue_list.append(self._queue_list[i])

            self._queue_list = new_queue_list
        self.write_queue_on_file()

    def swap(self, person1_id: str, person2_id: str):
        """
        Меняет местами двух людей
        :param person1_id: номер ИСУ первого
        :param person2_id: номер ИСУ второго
        :return: None
        """
        for index1 in range(len(self._queue_list)):
            if self._queue_list[index1].get_id() == person1_id:

                for index2 in range(len(self._queue_list)):
                    if self._queue_list[index2].get_id() == person2_id:
                        temp = self._queue_list[index1]
                        self._queue_list[index1] = self._queue_list[index2]
                        self._queue_list[index2] = temp

                        self.write_queue_on_file()

                        self.history.write(f"Поменялись местами: "
                                           f"{self._queue_list[index1].get_name()} <-> "
                                           f"{self._queue_list[index2].get_name()}"
                                           f" в {Date.get_time()}")

                        return

    @staticmethod
    def check_exist_in_queue(person_id, filename="queue.txt"):
        f = open(filename, "r", encoding="UTF-8")
        data = f.read().split("\n")
        for p in data:
            if p == "":
                continue
            p = p.split()
            _ID = p[0]

            if _ID == person_id:
                return True
        return False

    @staticmethod
    def check_person_passed(person_id, filename="queue.txt"):
        f = open(filename, "r", encoding="UTF-8")
        data = f.read().split("\n")
        for p in data:
            if p == "":
                continue
            p = p.split()
            _ID = p[0]

            if _ID == str(person_id):
                if p[3] == "True":
                    return True
                else:
                    return False

        return None

    def test(self):
        self.new_queue()
        return self.get_queue()
