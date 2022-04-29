import sys
import logging

from _modules.servicesProgram.TelegramBot import TelegramBot


class ProgramLogger:

    """
        Автор         : Макаров Алексей
        Описание      : Модуль для логгирования процесса выполнения программы
    """

    def __init__(self):

        """
            Автор      : Макаров Алексей
            Описание   : Магический метод,
                         выполняемый при инициализации объекта
        """

        self._telegramBot = TelegramBot()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)s] - %(message)s",
        )

    def logInfo(self, message: str) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Сведение о событии при выполнении программы
            Получаем  : {
                            varType: Str,
                            varName: message,
                            varDesc: Текст сообщения для отображения в логах
                        }
        """

        logging.info(message)

    def logError(self, message: str) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Сведение о критической ошибке при выполнении программы
            Получаем  : {
                            varType: Str,
                            varName: message,
                            varDesc: Текст сообщения для отображения в логах
                        }
        """

        logging.error(message)
        self._telegramBot.sendMessage(f"{message} - выполнение остановлено")
        sys.exit(1)
