from enum import Enum


class CommandEnum(Enum):

    # Вывод текущего режима
    now_mode = ["текущий режим", "режим", "mode", "now mode"]

    # Default mode
    # Расписание
    schedule = ["schedule", "расписание"]

    # Links
    get_journal_link = ["журнал", "journal"]

    # Работа с очередью
    # Main functions
    swap = ["поменять", "swap"]
    get_queue = ["очередь", "queue"]
    new_queue = ["новая очередь", "создай очередь", "new queue"]
    person_passed = ["прошел", "passed"]
    get_last_person_in_queue = ["предыдущий", "предыдущий в очереди", "last"]
    get_current_person_in_queue = ["сейчас", "current"]
    get_next_person_in_queue = ["следующий", "следующий в очереди", "next"]
    get_person_queue_position = ["место в очереди", "queue_position"]
    add_person = ["add", "добавиться", "+"]
    delete_person = ["delete", "удалиться", "-"]

    # Work with history
    get_history = ["history", "история"]

    # Requests
    swap_request = ["swap", "смена места в очереди", "смена"]


    # Вопросы (про Java и тд)
    get_java_question = ["java", "джава"]
    get_java_answer = ["ответ", "answer"]

    # Неизвестная команда
    unknown = ["unknown"]

    send_spam = ["сообщение для группы", "4all", "group message", "gm"]