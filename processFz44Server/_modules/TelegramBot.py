import requests


class TelegramBot:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для отправки критических уведомлений в телеграм
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """
        
        self.chatId   = "1807778017"
        self.botToken = "5313812895:AAFQy83OUL4asqFpJrJMbrT7P6GN99hpRAE"

    def sendMessage(self, message: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение отправки сообщения в чат
        """

        sendMessageUrl = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
            self.botToken, self.chatId, message
        )

        try:
            sendMessageResponseCode = requests.get(sendMessageUrl).status_code
            return 0 if sendMessageResponseCode == 200 else 1
        except Exception:
            return 2
