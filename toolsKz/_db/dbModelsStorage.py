from cmath import nan
from dataclasses import dataclass
import re
from enum import unique
from pymysql import Date
from sqlalchemy import DATE, Column

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
    name = Column(String(length = 500))
    inn = Column(String(length = 30))
    ogrn = Column(String(length = 50))
    address = Column(String(length = 500))
    placeName = Column(String(length = 100))
    placeIndex = Column(String(length = 10))
    contactEmail = Column(String(length = 100))
    contactPhone = Column(String(length = 50))
    contactPerson = Column(String(length = 100))
    licenseLink = Column(String(length = 100))
    licenseStatus = Column(SmallInteger())
    licenseNumber = Column(String(length = 50))
    licenseRegistered = Column(Date())
    licenseOrderNumber = Column(Integer())
    licenseOrderRegistered = Column(Date())
    licenseDuplicateNumber = Column(String(length = 50))
    licenseDuplicateRegistered = Column(Date())
    licenseTerminationReason = Column(String(length = 50))
    licenseTerminationRegistered = Column(Date())
    licenseCheckReason = Column(String(length = 50))
    licenseCheckDescription = Column(String(length = 1000))
    possibilitiesDesignWorks = Column(SmallInteger())
    possibilitiesEngineeringWorks = Column(SmallInteger())

    

    @validates(
        "name", 
    )
    def validateField(self, key, dataFieldValue) -> str:

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


class PostalCodes(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая почтовые индексы РФ
    """

    __tablename__ = "postalCodes"

    id = Column(Integer, primary_key = True)
    placeIndex = Column(String(length = 50), unique = True)
    placeCityName = Column(String(length = 100))
    placeRegionName = Column(String(length = 100))


def updateModelsStorage(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в БД
    """

    Base.metadata.create_all(dbConnection)

    return 0
