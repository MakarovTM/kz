import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer, Float

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RepublishedNotifications(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, содержащая
                    информацию о переопубликованных контрактах 
    """

    __tablename__ = "republished_notifications"

    id  = Column(Integer, primary_key = True)
    ikz = Column(String(length = 50), unique = True)
    obj = Column(String(length = 500))
    prc = Column(Float())
    crn = Column(String(length = 50))
    okv = Column(String(length = 500))
    rid = Column(Integer, ForeignKey("republished_notifications.id"))
    pnb = Column(String(length = 20))
    pdt = Column(DateTime)


class ContractProjectTimeLine(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    хронологию процесса заключение контракта
    """

    __tablename__ = "contract_project_timeline"

    id  = Column(Integer, primary_key = True)
    pnb = Column(String(length = 50), unique = True)
    hpb = Column(Boolean())
    hch = Column(Boolean())
    hsg = Column(Boolean())
    hcl = Column(Boolean())
    hcf = Column(Boolean())
    cdt = Column(DateTime, default = datetime.datetime.utcnow)


class PurchasesFinalProtocol(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    информацию о статусе подведения результатов преведения закупки
    """

    __tablename__ = "purchasesFinalProtocol"

    id  = Column(Integer, primary_key = True)
    num = Column(String(length = 50), unique = True)
    fcd = Column(String(length = 50))


def main(db_connection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в базе данных
    """

    Base.metadata.create_all(db_connection)

    return 0
