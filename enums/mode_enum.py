from enum import Enum


class ModeEnum(Enum):
    QUESTION = ["режим вопросов", "вопросы", "вопрос", "questions"]

    QUEUE = ["режим очереди", "очередь", "queue"]
    DEFAULT = ["обычный режим", "default", "обычный", "выйти", "закончить"]
    REQUEST = ["режим заявки", "заявка", "request"]
    GET_NUMBER = ["GET NUMBER"]     # програмный мод
    YES_NO_ASK = ["YES NO ASK"]     # програмный мод
    UNKNOWN = ["Unknown"]           # програмный мод

