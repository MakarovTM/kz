import requests

from pathlib import Path
from configparser import ConfigParser


class ProgramTelegramBot:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для отправки критических уведомлений в телеграм
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        self._config = ConfigParser()
        self._config.read(f"{Path(__file__).parents[2]}/config.ini")

    def sendMessage(self, message: str) -> int:

        """
            Автор     : Макаров Алексей
            Описание  : Выполнение отправки сообщения в чат
            Получаем  : {
                            varType: Str,
                            varName: message,
                            varDesc: Сообщение для отправки в телеграм чат
                        }
            Возвращем : {
                            varType: Int,
                            varDesc: 0 - Сообщение успешно отправлено
                                     1 - Ошибка при отправке сообщения
                        }
        """

        try:
            if requests.get(
                "https://api.telegram.org/bot{}/sendMessage".format(
                    self._config["telegramBot"]["botToken"]
                ),
                params={
                    "text": message,
                    "chat_id": self._config["telegramBot"]["chatId"],
                }
            ).status_code != 200:
                return 1
        except Exception:
            return 1

        return 0
