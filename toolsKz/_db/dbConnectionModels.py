from cmath import nan
from dataclasses import dataclass
import re
from enum import unique
from pymysql import Date
from sqlalchemy import Column

from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import Date, DateTime

from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class LicensesMinCulture(Base):

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
    licenseFrom = Column(Date())
    licenseTill = Column(Date())
    licenseNumber = Column(String(length = 25))

    @validates("orgOgrn", "licenseFrom", "licenseTill", "orgName", "orgInn", "licenseNumber")
    def validateDateField(self, key, dataFieldValue) -> str:

        if key == "orgName" or key == "licenseNumber":

            if len(str(dataFieldValue)) < 5:
                return ""
            else:
                return dataFieldValue

            return ""

        if key == "orgOgrn" or key == "orgInn":

            if re.fullmatch(r"\d+", str(dataFieldValue)):
                return dataFieldValue

            return ""

        if key == "licenseFrom" or key == "licenseFrom":

            if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z", str(dataFieldValue)):
                return dataFieldValue[:10]
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(dataFieldValue)):
                return dataFieldValue
            
            return "0000-00-00"

        return ""

def updateModelsStorage(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в БД
    """

    Base.metadata.create_all(dbConnection)

    return 0
