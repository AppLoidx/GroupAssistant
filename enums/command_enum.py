from enum import Enum


class CommandEnum(Enum):

    # Расписание
    schedule = ["schedule", "расписание"]

    # Вывод текущего режима
    now_mode = ["текущий режим", "режим", "mode", "now mode"]
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

    # Work with history
    get_history = ["history", "история"]

    # Requests
    swap_request = ["swap", "смена места в очереди", "смена"]
    add_person_request = ["add_person"]
    delete_person_request = ["delete_person"]

    # Вопросы (про Java и тд)
    java_question = ["java"]

    # Неизвестная команда
    unknown = ["unknown"]
