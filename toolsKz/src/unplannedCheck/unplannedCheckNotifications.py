import datetime
import requests


UNPLANNED_CHECKS_PUBLISHED = datetime.date.today().strftime("%d.%m.%Y")
UNPLANNED_CHECKS_NOTIFICATIONS_RECIPIENTS = [
    "akulov@trade.su",
    "pzm@contract-center.ru"
]


def getRequest(url) -> str:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение GET - запроса
    """

    response = requests.get(url)

    return response.text if response.status_code == 200 else ""

def publishedUnplannedChecks() -> list:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение запроса на список проверок,
                    опубликованных на момент запуска скрипта
    """

    def requestUnplannedChecks(url: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сетевого
                        запроса на получение страницы
                        с опубликованными внеплановыми проверками
        """

        response = requests.get(url)

        return response.text if response.status_code == 200 else ""


    def processParsedUnplannedChecks()





def main() -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Точка входа в инструмент 
                    по выполнение уведомления менеджера 
                    о появлении незапланированной проверки УФАС
    """

    return 0
