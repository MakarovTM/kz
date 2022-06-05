from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.servicesProgram.ProgramConfig import ProgramConfig
from modules.servicesServer.ServerVm20ViaSSH import ServerVm20ViaSSH

from db.DbModelsStorage import updateDbStructure


class DbConnection:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с базой данных
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self._config = ProgramConfig()
        self._vm20ServerConnection = ServerVm20ViaSSH()

        self._dbHost = self._config.getItem("vm20TradeSuDb", "host")
        self._dbUser = self._config.getItem("vm20TradeSuDb", "user")
        self._dbName = self._config.getItem("vm20TradeSuDb", "dbName")

        self._dbConnection = None
        self._dbConnectionSession = None

        if self.__createDbConnection() != 0:
            print("Ошибка подключения к БД")

    def __createDbConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с БД на сервере vm20.trade.su
        """

        try:
            self._dbConnection = create_engine(
                "mysql+pymysql://{}@{}:{}/{}".format(
                    self._dbUser,
                    self._dbHost,
                    self._vm20ServerConnection.showLocalBindPort(),
                    self._dbName
                ),
                pool_recycle=3600
            )
            session = sessionmaker(bind=self._dbConnection)
            self._dbConnectionSession = session()
        except Exception as e:
            print(e)
            return 1

        return 0

    def commitDbConnectionSession(self):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        self._dbConnectionSession.commit()

    def updateDbModelStorage(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обновления структуры БД
        """

        updateDbStructure(self._dbConnection)
        self.commitDbConnectionSession()
