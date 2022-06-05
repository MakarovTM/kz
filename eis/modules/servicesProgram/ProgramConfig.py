from pathlib import Path
from typing import Union
from configparser import ConfigParser


class ProgramConfig:

    """
        Автор:      Макаров Алексей
        Описание:   Модуль по работе с конфигурационным файлом
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self._config = ConfigParser()

        self._config.read(f"{Path(__file__).parents[2]}/config.ini")

    def getItem(self, root: str, inRoot: str) -> Union[str, None]:

        """
            Автор:      Макаров Алексей
            Описание:   Получение значение по
                        переданному ключу из конфигурационного файла
        """

        if self._config.has_option(root, inRoot):
            return self._config.get(root, inRoot)
        return None
