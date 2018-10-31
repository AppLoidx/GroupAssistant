class File:

    @staticmethod
    def safe_open(filename, mode="r", encoding="UTF-8"):
        """

        Безопасное открытие файла.
        FIleNotFoundError - если файл не найден, то создает её

        :param filename: Имя файла
        :param mode: Режим открытия
        :param encoding: Кодировка
        :return: IO
        """
        try:
            file = open(filename, mode, encoding=encoding)
        except FileNotFoundError:
            file = open(filename, "w", encoding=encoding)
            file.close()
            file = open(filename, mode, encoding=encoding)

        return file