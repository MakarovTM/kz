from dbfread import DBF
from typing import Dict, List

from _db.dbConnection import dbConnection
from _db.dbModelsStorage import PostalCodes

from _modules.ServerViaSsh import ServerViaSsh


class ParsingPostalCodes:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение парсинга данных о почтовых индексах РФ
        Источник:       https://www.pochta.ru/support/database/ops    
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self._dbConnection = None
        self._dbServerConnection = None

        self.postalCodesData: List[Dict] = []
        self.pathPostalCodeDb = "/Users/makarov/Downloads/PIndx07.dbf"

    def __del__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при деинициализации объекта
        """

        self.__deleteDbOnServerConnection()
        self.__deleteDbServerConnection()

    def __createDbServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения с сервером БД
        """

        self._dbServerConnection = ServerViaSsh(
            "vm20.trade.su", 7023,
            "alexey_external", "sUvT4A6n",
            "192.168.0.121", 3306
        )

        self._dbServerConnection.createConnection()

        return 0

    def __deleteDbServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Разрушение соединения с сервером БД
        """

        self._dbServerConnection.deleteConnection()

        return 0

    def __createDbOnServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключение с БД, расположенной на сервере
        """

        self._dbConnection = dbConnection(
            "localhost",
            self._dbServerConnection.serverConnection.local_bind_port,
            "rosexport"
        )
        self._dbConnection.createConnection()
        self._dbConnection.createConnectionSession()
        self._dbConnection.updateModelsStorage()

        return 0

    def __deleteDbOnServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Разрушение соединения с БД, расположенной на сервере
        """

        self._dbConnection.deleteConnection()

        return 0

    def __retrievalData(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
            Возвращаем: 0 - Извлечение данных выполнено успешно
        """

        for record in DBF(self.pathPostalCodeDb):
            self.postalCodesData.append({
                "placeIndex": record["INDEX"],
                "placeCityName": record["CITY"] if record["CITY"] != "" else record["REGION"],
                "placeRegionName": record["REGION"],
            })

        return 0

    def __saveDataToDb(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        for postalCode in self.postalCodesData:
            pass

        return 0

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса парсинга сведение о почтовых индексах РФ
        """

        if self.__createDbServerConnection() == 0:
            if self.__createDbOnServerConnection() == 0:
                if self.__retrievalData() == 0:
                    print(self.postalCodesData)

        return 0
