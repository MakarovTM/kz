import configparser

from pathlib import Path

from _modules.ServerViaSsh import ServerViaSsh


class UpdateOrgsContacts:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обновления 
                        реестра компаний для быстрого поиска контактов по ИНН
    """

    def __init__(self) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self._config = configparser.ConfigParser()
        self._rootPath = Path(__file__).parents[2]

    def __readConfigFile(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение чтения конфигурационного файла
        """

        try:
            self._config.read(f"{self._rootPath}/config.ini")
        except Exception as e:
            print("Произошла ошибка при чтении файла конфигурации")

        return 0

    def __createDbServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение подключения 
                        к серверу, на котором расположена БД
        """

        self._dbServerConnection = ServerViaSsh(
            self._config["vm20TradeServer"]["host"], self._config["vm20TradeServer"]["port"],
            self._config["vm20TradeServer"]["user"], self._config["vm20TradeServer"]["pasw"],
            self._config["vm20TradeServerDb"]["dbHost"], self._config["vm20TradeServerDb"]["dbPort"],
        )

        if self._dbServerConnection.createConnection() != 0:
            print("Произошла ошибка при попытке подключения к серверу, на котором расположена БД")

        return 0


    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обновление реестра компаний
        """

        if self.__readConfigFile() == 0:
            print("ok")

        return 0
