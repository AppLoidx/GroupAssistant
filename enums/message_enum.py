from enum import Enum


class MessageEnum(Enum):

    send_to_group = "send_to_group"
    send_to_person = "send_to_person"

    from_group = "from_group"
    from_person = "from_person"

    unknown = "unknown"
