from editor.json_file import JSONFile
from parser_m.parser import Parser
import requests

import datetime

class Date(Parser):

    def __init__(self):

        super().__init__()
        self.days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        self.base_day = 7    # Нечетная

    @staticmethod
    def get_time():
        res = requests.get("http://api.timezonedb.com/v2.1/get-time-zone?"
                           "key=CJ8I7RTKYXDD&"
                           "by=zone&"
                           "zone=Europe/Moscow&"
                           "format=json")
        res = res.json()
        return res['formatted'].split()[1]

    @staticmethod
    def get_week_parity():
        """
        Возвращает четность недели
        :return: Четная/Нечетная
        """
        # b_site = self.set_http("http://www.ifmo.ru/ru/schedule/0/P3112/raspisanie_zanyatiy_P3112.htm")
        #
        # return self.clean_all_tag_from_str(b_site.select(".schedule-week")[0].find("strong"))

        today_day, month = map(int, datetime.datetime.today().strftime("%d %m").split())

        if month != 11:
            today_day += JSONFile.read_json("schedule/2018_month.json")[str(month)]
        if ((today_day - 5) // 7) % 2 == 0:
            return "Нечетная"
        else:
            return "Четная"

    def get_day_of_week(self):
        return self.days[datetime.datetime.today().weekday()]

