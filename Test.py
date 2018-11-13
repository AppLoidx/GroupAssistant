from editor.json_file import JSONFile
from enums.mode_enum import ModeEnum
from group_queue.queue import Queue
from manual.manual import Manual
from parser_m.date import Date
import requests
import bs4

import sys

queue = Queue("groups_list/P3112.json")

queue.new_queue()
queue.write_queue_on_file()
queue.update_queue()