from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from _db.DbModelsStorage import updateDbStructure


class DbConnection:

    """
        Автор:          Макаров Алексей
        Описание:       Програмный модуль,
                        контролирующий работу с базой данных
    """

    def __init__(
        self,
        dbHost: str, dbPort: int, dbUser: str, dbName: str,
        dbPasw=None
    ) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        if self.cСonstructed:

            self._host = dbHost
            self._port = dbPort
            self._user = dbUser
            self._pasw = dbPasw
            self._dbName = dbName

            self.cСonstructed = True

            self._dbConnection = None
            self.dbConnectionSession = None

    def __new__(cls, *args, **kwargs):

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при создании объекта
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DbConnection, cls).__new__(cls)
            cls.instance.cСonstructed = True

        return cls.instance

    def createDbConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения к БД
        """

        try:
            if self._pasw is None:
                self._dbConnection = create_engine(
                    "mysql+pymysql://{}@{}:{}/{}".format(
                        self._user,
                        self._host,
                        self._port,
                        self._dbName
                    ),
                    pool_recycle=3600
                )
            else:
                pass
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
            self.commitDbConnectionSession()
