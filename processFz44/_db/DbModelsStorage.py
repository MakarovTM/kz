from ast import Str
from sqlalchemy import Column, SmallInteger

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ContractProjectsPublished(Base):

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


class ContractProjectChanged(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    выложенные на FTP сервер изменения в проектах контрактов
    """

    id = Column(Integer, primary_key = True)
    contractNum = Column(String(length = 50))
    contractTsm = Column(DateTime())
    acceptedAll = Column(SmallInteger())


class ContractProjectSigned(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая
                    выложенные на FTP сервер подписанные проекты контрактов
    """

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
