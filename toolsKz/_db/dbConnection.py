from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from _db.dbConnectionModels import updateModelsStorage


class dbConnection:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с базой данных
    """

    def __init__(self, host: str, port: str, user: str) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при создании объекта
        """

        self.host = host
        self.port = port
        self.user = user

        self.dbConnection = None
        self.dbConnectionSession = None

    def createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключение к БД
        """

        self.dbConnection = create_engine(
            "mysql+pymysql://{user}@{host}:{port}/protocols_records".format(
                user = self.user,
                host = self.host, port = self.port,
            )
        )

        return 0
    
    def createConnectionSession(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание сессии подключения к БД
        """

        session = sessionmaker(bind = self.dbConnection)
        self.dbConnectionSession = session()

        return 0

    def deleteConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Удаление соединения с БД
        """
        
        if self.dbConnection is not None:
            self.dbConnection.dispose()
        
        return 0

    def commitSession(self) -> int:

        self.dbConnectionSession.commit()

    def updateModelsStorage(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Обновление списка моделей в БД
        """

        if self.dbConnection is not None:
            updateModelsStorage(self.dbConnection)
