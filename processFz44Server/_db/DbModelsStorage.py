from enum import unique
from sqlalchemy import Column, ForeignKey

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import Date, DateTime

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ContractProjectsProtocolPublished(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    выложенные на FTP сервер проекты контрактов
    """

    __tablename__ = "contractProjectsPublished"

    id = Column(Integer, primary_key = True)
    contractNum = Column(String(length = 50))
    contractPub = Column(DateTime())
    contractObj = Column(Text())
    contractPrc = Column(Float(10, 2))
    customerInn = Column(String(length = 50))
    supplierInn = Column(String(length = 50))


class ContractProjectProtocolChanged(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    выложенные на FTP сервер изменения в проектах контрактов
    """

    __tablename__ = "сontractProjectChanged"

    id = Column(Integer, primary_key = True)
    contractNum = Column(String(length = 50))
    contractTsm = Column(DateTime())
    acceptedAll = Column(SmallInteger())


class ContractProjectProtocolSigned(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    выложенные на FTP сервер подписанные проекты контрактов
    """

    __tablename__ = "сontractProjectSigned"

    id = Column(Integer, primary_key = True)
    contractNum = Column(String(length = 50))
    contractTsm = Column(DateTime())


class ContractProjectProtocolCancel(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая выложенные на FTP сервер 
                    файлы с информацией об отмене процедуры заключения контракта
    """

    __tablename__ = "сontractProjectCancel"

    id = Column(Integer, primary_key = True)
    contractNum = Column(String(length = 50))
    contractTsm = Column(DateTime())


class NotificationProtocolsPublished(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая выложенные на FTP 
                    сервер файлы с информацией о опубликованных в ЕИС
    """

    __tablename__ = "notificationProtocolsPublished"

    id = Column(Integer, primary_key = True)

    purchaseNum = Column(String(length = 50), unique = True)
    purchaseTsm = Column(Date())
    purchaseObj = Column(String(length = 1000))
    purchaseIkz = Column(String(length = 50))
    customerInn = Column(String(length = 20))


class PlanGraphsPurchasesPublished(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая выложенные на FTP сервер файлы 
                    с информацией о запланированной процедуре проведения закупки
    """

    __tablename__ = "planGraphsPurchasesPublished"

    id = Column(Integer, primary_key = True)
    purchaseIkz = Column(String(length = 50), unique = True)
    purchaseOkv = Column(String(length = 500))
    purchaseObj = Column(String(length = 1000))
    purchasePrc = Column(Float())
    purchaseSim = Column(ForeignKey("planGraphsPurchasesPublished.id"))

def mainUpdateModels(db_connection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в базе данных
    """

    Base.metadata.create_all(db_connection)

    return 0
