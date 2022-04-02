from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.DB_Models import main as dm_models_main


class DB_Connection:

    """
        Автор:      Макаров Алексей
        Описание:   Модуль, контролирующий подключение к локальной БД
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по работе с БД
        """

        if(self.__initialized): return
        self.__initialized = True

        self.dbConnection = None
        self.dbConSession = None
        self.dbConSessionItems = []
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB_Connection, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def makeConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с БД
        """

        self.dbConnection = create_engine(
            "mysql+mysqlconnector://alderson:pops3@62.113.97.50:3306/tenders_master?auth_plugin=mysql_native_password",
            pool_recycle = 3600
        )

        print(dm_models_main(self.dbConnection))

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

        self.dbConSession.commit()
