import pickle
import configparser
from pathlib import Path

from _db.dbConnection import dbConnection
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

    def __del__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при деструктуризации объекта
        """

        if self.__deleteDbOnServerConnection() == 0:
            self.__deleteDbServerConnection()

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

    def __deleteDbServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение удаления соединения 
                        с сервером, на котором расположена БД
        """

        if self._dbServerConnection.deleteConnection() != 0:
            print("Произошла ошибка при разрушении соединения с удаленным сервером")

        return 0

    def __createDbOnServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение подключения
                        к БД, расположенной на сервере
        """

        self._dbOnServerConnection = dbConnection(
            "localhost",
            self._dbServerConnection.serverConnection.local_bind_port,
            "rosexport"
        )

        if self._dbOnServerConnection.createConnection() == 0:
            if self._dbOnServerConnection.createConnectionSession() != 0:
                print("Произошла ошибка при создании активной сессии с БД")
        else:
            print("Произошла ошибка при попытке подключения к БД, которая расположена на сервере")

        return 0

    def __deleteDbOnServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение удаления соединения с БД
        """

        if self._dbOnServerConnection.deleteConnection() != 0:
            print("Произошла ошикаб при удалении соединения с БД, расположенной на сервере")
        
        return 0

    def __fetchOrganizationContacts(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполннение извлечения 
                        информации о контактах компаний из БД
        """

        self._orgsContacts = {
            resultRow[0]: {
                "contactPerson": resultRow[1],
                "contactEmail":  resultRow[2],
                "contactPhone":  resultRow[3],
            }
            for resultRow in self._dbOnServerConnection.dbConnectionSession.execute(
                """
                    SELECT 
                        DISTINCT(inn), contact_person_name, mail, phone 
                    FROM 
                        protocols_records.legal_entity_table
                """
            )
        }

        return 0

    def __fetchOrganizationContactsSave(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения извлеченных данных в БД
        """

        with open(f"{self._rootPath}/vars/baseOrgsContacts.pkl", "wb") as dbFile:
            pickle.dump(self._orgsContacts, dbFile)

        return 0

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обновление реестра компаний
        """

        if self.__readConfigFile() == 0:
            if self.__createDbServerConnection() == 0:
                if self.__createDbOnServerConnection() == 0:
                    if self.__fetchOrganizationContacts() == 0:
                        if self.__fetchOrganizationContactsSave() == 0:
                            print("Выполнение обновления данных успешно выполнено")

        return 0
