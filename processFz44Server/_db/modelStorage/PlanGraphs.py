from sqlalchemy import event

from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from _db.DbModelsStorage import Base


class PlanGraphs(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая план - графики закупок
    """

    __tablename__ = "planGraphs"

    id = Column(Integer, primary_key=True)
    purchaseIkz = Column(String(length=50), unique=True)
    customerInn = Column(String(length=50))
    purchaseObj = Column(String(length=1000))
    purchasePrc = Column(Float(10, 2))
    referenceTo = Column(Integer, ForeignKey("planGraphs.id"))


@event.listens_for(PlanGraphs, "before_insert")
def setCustomerInn(mapper, connection, target):

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение извлечения
                    ИНН заказчика перед сохранением данных
    """

    target.customerInn = target.purchaseIkz[3:13]
