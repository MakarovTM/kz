from pathlib import Path
from configparser import ConfigParser


class ProgramConfig:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль содержащий
                        информацию из конфигурационного файла
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self.config = ConfigParser()
        self.config.read(f"{Path(__file__).parents[2]}/config.ini")
