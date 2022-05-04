from sqlalchemy import event

from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from sqlalchemy.orm import validates

from _db.DbModelsStorage import Base


class EpNotifications(Base):

    """
        Автор:          Макаров Алексей
        Описание:       Модель данных, описывающая размещенные уведомлении
                        об осуществлении проведения процедуры закупки
    """

    __tablename__ = "epNotifications"

    id = Column(Integer, primary_key=True)
    purchaseNum = Column(String(length=50), unique=True)
    purchaseObj = Column(String(length=1000))
    purchasePrc = Column(Float(10, 2))
    placingFrom = Column(Date())
    placingTill = Column(Date())
    customerInn = Column(String(length=30))
    purchaseIkz = Column(String(length=50))
    publishedEIS = Column(Date())

    @validates("placingFrom", "placingTill", "publishedEIS")
    def validateColumnValue(self, columnName, columnValue):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение форматирования данных при записи в БД
        """

        if columnName in ("placingTill", "placingFrom", "publishedEIS"):
            return columnValue[:10]


@event.listens_for(EpNotifications, "before_insert")
def setCustomerInn(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения
                        ИНН заказчика перед сохранением данных
    """

    target.customerInn = target.purchaseIkz[3:13]
