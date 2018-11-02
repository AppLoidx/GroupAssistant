from editor.json_file import JSONFile
from enums.mode_enum import ModeEnum
from group_queue.queue import Queue
from manual.manual import Manual
from parser_m.date import Date

print(Manual.get_manual(ModeEnum.QUEUE))