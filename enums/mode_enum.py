from enum import Enum


class ModeEnum(Enum):

    QUESTION = ["режим вопросов", "вопросы", "вопрос", "questions", "question"]

    QUEUE = ["режим очереди", "очередь", "queue"]
    DEFAULT = ["обычный режим", "default", "обычный", "выйти", "закончить"]
    REQUEST = ["режим заявки", "заявка", "request"]
    SETTINGS = ["режим настроек", "settings", "set"]
    LINK = ["режим ссылок", "ссылки", "links", "link"]

    GET_NUMBER = ["GET NUMBER"]     # програмный мод
    YES_NO_ASK = ["YES NO ASK"]     # програмный мод
    GET_STRING = ["GET STRING"]

    UNKNOWN = ["Unknown"]           # програмный мод

