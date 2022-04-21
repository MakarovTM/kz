from enum import unique
from sqlalchemy import Column

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import DateTime

from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class licensesMinCulture(Base):

    """
        Автор:          Макаров Алексей
        Описание:       Модель данных, описывающая лицензии, 
                        выданные мин. культуры на осуществление 
                        деятельности по сохранению объектов культурного наследия
    """

    __tablename__ = "licensesMinCulture"

    id = Column(Integer, primary_key = True)
    orgName = Column(String(length = 50))
    orgInn  = Column(String(length = 30), unique = True)
    orgOgrn = Column(String(length = 50))
    licenseFrom = Column(DateTime())
    licenseTill = Column(DateTime())
    licenseNumber = Column(String(length = 25))

    @validates("licenseTill")
    def validateLicenseFrom(self, key, licenseFrom) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сверки формата даты перед записью в БД
        """

        return licenseFrom


def updateModelsStorage(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в БД
    """

    Base.metadata.create_all(dbConnection)
