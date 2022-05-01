from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def updateDbStructure(dbConnection):

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обновления структуры БД
    """

    Base.metadata.create_all(dbConnection)
