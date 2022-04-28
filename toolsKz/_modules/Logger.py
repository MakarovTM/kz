import sys
import logging


class Logger:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для логгирования процесса выполнения программы
    """

    def __new__(cls):

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при создании объекта 
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(Logger, cls).__new__(cls)
            cls.instance.cСonstructed = False

        return cls.instance

    def __init__(self):
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        if not self.cСonstructed:

            # self.telegramBot  = TelegramBot()
            self.cСonstructed = True

            logging.basicConfig(
                level  = logging.INFO,
                format = "%(asctime)s - [%(levelname)s] - %(message)s",
            )

    def logInfo(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Сведение о событии при выполнении программы
        """

        logging.info(message)

    def logError(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Сведение об ошибке при выполнении программы
        """

        logging.error(message)

    def logCritError(self, message: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Сведение об ошибке при выполнении программы
        """

        logging.critical(message)
        sys.exit(1)
        # self.telegramBot.sendMessage(message)
