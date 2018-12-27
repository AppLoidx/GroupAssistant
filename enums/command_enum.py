from enum import Enum


class CommandEnum(Enum):

    # Common
    one = [1, "1"]
    two = [2, "2"]
    three = [3, "3"]
    four = [4, "4"]
    five = [5, "5"]
    six = [6, "6"]

    # Вывод текущего режима
    now_mode = ["текущий режим", "режим", "mode", "now mode"]

    # help
    help = ["help", "хелп", "man"]

    # Default mode
    # Расписание
    schedule = ["schedule", "расписание"]

    # Links
    get_journal_link = ["журнал", "journal"]
    get_group_link = ["группа", "group"]

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

    # Settings
    show = ["show", "settings"]
    change_push = ["push"]

    # Неизвестная команда
    unknown = ["unknown"]

    send_spam = ["сообщение для группы", "4all", "group message", "gm"]
