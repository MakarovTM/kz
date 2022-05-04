from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pathlib import Path
from configparser import ConfigParser

from _db.DbModelsStorage import updateDbStructure


class DbConnection:

    """
        Автор:          Макаров Алексей
        Описание:       Програмный модуль,
                        контролирующий работу с базой данных
    """

    def __init__(self, dbName: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        if not self.cСonstructed:

            self._config = ConfigParser()
            self._config.read(f"{Path(__file__).parents[1]}/config.ini")

            self._host = self._config[dbName]["host"]
            self._port = self._config[dbName]["port"]
            self._user = self._config[dbName]["user"]
            self._pasw = self._config[dbName]["pasw"]
            self._dbName = self._config[dbName]["dbName"]

            self.cСonstructed = True

            self._dbConnection = None
            self.dbConnectionSession = None

    def __new__(cls, *args):

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при создании объекта
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DbConnection, cls).__new__(cls)
            cls.instance.cСonstructed = False

        return cls.instance

    def createDbConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения к БД
        """

        try:
            self._dbConnection = create_engine(
                "mysql+pymysql://{}:{}@{}:{}/{}".format(
                    self._user, self._pasw,
                    self._host, self._port, self._dbName
                ),
                pool_recycle=3600
            )
            session = sessionmaker(bind=self._dbConnection)
            self.dbConnectionSession = session()
            self.updateDbModelStorage()
        except Exception as e:
            print(e)
            return 1

        return 0

    def commitDbConnectionSession(self):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        self.dbConnectionSession.commit()

    def updateDbModelStorage(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обновление структуры БД
        """

        if updateDbStructure(self._dbConnection) == 0:
            print("Струтура базы данных обновлена")
