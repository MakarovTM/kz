from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from _db.DbModelsStorage import mainUpdateModels


class DbConnection:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль, контролирующий подключение к локальной БД
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        if not self.cСonstructed:

            self.cСonstructed = True

            self.dbConnection = None
            self.dbConSession = None
            self.dbConSessionItems = []
    
    def __new__(cls):

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при создании объекта
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DbConnection, cls).__new__(cls)
            cls.instance.cСonstructed = False

        return cls.instance

    def __del__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при удалении объекта
        """

        self.__deleteConnection()

    def __deleteConnection(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Закрываем соединение с базой данных
        """

        if self.dbConnection is not None:
            self.dbConnection.dispose()

    def makeConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с БД
        """

        self.dbConnection = create_engine(
            "mysql+pymysql://makarov:makarov@62.113.97.50:3306/fz44",
            pool_recycle = 7200
        )

        return 0

    def makeConnectionSession(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание сессии подключения к базе данных
        """

        session = sessionmaker(bind = self.dbConnection)

        self.dbConSession = session()

        return 0

    def commitSession(self):

        self.dbConSession.bulk_save_objects(self.dbConSessionItems)
        self.dbConSession.commit()


    def updateDataBaseModels(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Обновления структуры базы данных
        """

        if mainUpdateModels(self.dbConnection) == 0:
            print("Структура базы данных успешно обновлена")

        return 0
