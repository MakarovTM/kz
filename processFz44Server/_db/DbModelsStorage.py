from sqlalchemy import Column

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import DateTime

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


def mainUpdateModels(db_connection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в базе данных
    """

    Base.metadata.create_all(db_connection)

    return 0
