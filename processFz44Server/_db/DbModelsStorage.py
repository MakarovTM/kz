from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from _db.modelStorage.PurchaseNotifications import PurchaseNotifications
from _db.modelStorage.PurchaseProtocolsFinal import PurchaseProtocolsFinal


def updateDbStructure(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обновления структуры БД
    """

    Base.metadata.create_all(dbConnection)

    return 0
