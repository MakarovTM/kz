from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from _db.modelStorage.PlanGraphs import PlanGraphs
from _db.modelStorage.EpNotifications import EpNotifications
from _db.modelStorage.PurchaseProtocolFinal import PurchaseProtocolFinal
from _db.modelStorage.ZakupkiFilesProcessingStatus import ZakupkiFilesProcessingStatus


def updateDbStructure(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обновления структуры БД
    """

    Base.metadata.create_all(dbConnection)

    return 0
