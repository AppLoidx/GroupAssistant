from parser_m.parser import Parser
import requests


class Date(Parser):

    def __init__(self):

        super().__init__()

    @staticmethod
    def get_time():
        res = requests.get("http://api.timezonedb.com/v2.1/get-time-zone?"
                           "key=CJ8I7RTKYXDD&"
                           "by=zone&"
                           "zone=Europe/Moscow&"
                           "format=json")
        res = res.json()
        return res['formatted'].split()[1]

    def get_week_parity(self):
        """
        Возвращает четность недели
        :return: Четная/Нечетная
        """
        b_site = self.set_http("http://www.ifmo.ru/ru/schedule/0/P3112/raspisanie_zanyatiy_P3112.htm")

        return self.clean_all_tag_from_str(b_site.select(".schedule-week")[0].find("strong"))
