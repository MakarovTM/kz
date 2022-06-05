import logging


class ProgramLogger:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для логгирования
                        процесса выполнения программы
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

    def logInfo(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Лог с информацией о выполнении программы
        """

        logging.info(message)

    def logError(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Лог с информацией об ошибке при выполнении программы
        """

        logging.error(message)

    def logCriticalError(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Лог с информацией
                        о критической ошибке при выполнении программы
        """

        logging.critical(f"{message} - выполнение программы остановлено")
