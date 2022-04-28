from email.mime import base
from enum import unique
from sqlalchemy import Column
import math
import re
import json
import pickle
from pathlib import Path
from sqlalchemy import String
from sqlalchemy import Integer, SmallInteger
from sqlalchemy import Date

from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


with open(
    f"{Path(__file__).parents[1]}/vars/basePostalCodes.pkl", "rb") as file:
        basePostalCodes = pickle.load(file)


with open(
    f"{Path(__file__).parents[1]}/vars/baseOrgsContacts.pkl", "rb") as file:
        baseOrgsContacts = pickle.load(file)


class LicensesMinCulture(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая лицензии, 
                    выданные мин. культуры на осуществление 
                    деятельности по сохранению объектов культурного наследия
    """

    __tablename__ = "licensesMinCulture"

    id = Column(Integer, primary_key = True)
    licenseId = Column(Integer, unique = True)
    name = Column(String(length = 500))                     # ln: 74
    inn = Column(String(length = 30))                       # ln: 79
    ogrn = Column(String(length = 30))                      # ln: 79
    address = Column(String(length = 500))                  # ln: 74
    placeName = Column(String(length = 100))                # ln: 105
    placeIndex = Column(String(length = 10))                # ln: 87
    contactEmail = Column(String(length = 100))             # ln: 127
    contactPhone = Column(String(length = 50))              # ln: 127
    contactPerson = Column(String(length = 100))            # ln: 127
    licenseLink = Column(String(length = 100))              # ln: 74
    licenseStatus = Column(SmallInteger())                  # ln: 79
    licenseNumber = Column(String(length = 50))             # ln: 74
    licenseRegistered = Column(Date())                      #
    licenseOrderNumber = Column(Integer())                  # ln: 79
    licenseOrderRegistered = Column(Date())                 #
    licenseDuplicateNumber = Column(String(length = 50))    # ln: 74
    licenseDuplicateRegistered = Column(Date())             #
    licenseTerminationReason = Column(String(length = 50))  # ln: 74
    licenseTerminationRegistered = Column(Date())           # 
    licenseCheckReason = Column(String(length = 500))       # ln: 90
    licenseCheckDescription = Column(String(length = 1000)) # ln: 74
    possibilitiesDesignWorks = Column(SmallInteger())       # ln: 96
    possibilitiesEngineeringWorks = Column(SmallInteger())  # ln: 96

    @validates("name", "address", "licenseLink", "licenseNumber", "licenseDuplicateNumber", "licenseTerminationReason", "licenseCheckDescription","inn", "ogrn", "licenseStatus", "licenseOrderNumber", "licenseCheckReason", "possibilitiesDesignWorks", "possibilitiesEngineeringWorks", "licenseRegistered", "licenseOrderRegistered", "licenseDuplicateRegistered", "licenseTerminationRegistered")
    def validateColumnValue(self, columnName, columnValue):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение проверки записываемого в БД поля
        """

        if columnName in [
            "name", "address", "licenseLink", "licenseNumber", "licenseDuplicateNumber", "licenseTerminationReason", "licenseCheckDescription"]:
            if str(columnValue) == "nan":
                return None
            else:
                return columnValue

        if columnName in ["inn", "ogrn", "licenseStatus", "licenseOrderNumber"]:
            if str(columnValue) == "nan":
                return None
            else:
                if re.fullmatch(r"\d+", str(columnValue)):
                    return columnValue
                else:
                    return None

        if columnName in ["licenseCheckReason"]:
            if str(columnValue) == "nan":
                return None
            else:
                return json.loads(columnValue)[0]["statement"]

        if columnName in ["possibilitiesDesignWorks", "possibilitiesEngineeringWorks"]:
            if str(columnValue) == "nan":
                return 0
            else:
                if columnValue:
                    return 1

        if columnName in ["licenseRegistered", "licenseOrderRegistered", "licenseDuplicateRegistered", "licenseTerminationRegistered"]:
            if str(columnValue) == "nan":
                return None
            else:
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z", str(columnValue)):
                    return columnValue[:10]
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(columnValue)):
                    return columnValue
                return "0000-00-00"
            



@event.listens_for(LicensesMinCulture, "before_insert")
def setPostalIndex(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения 
                        индекса города из адреса и запись в `placeIndex` 
    """

    if str(target.address) == "nan" or target.address is None:
        target.placeIndex = None
    else:
        if foundAddressIndex := re.findall(r"\d{6}", target.address):
            target.placeIndex = foundAddressIndex[0]
        else:
            target.placeIndex = None


@event.listens_for(LicensesMinCulture, "before_insert")
def setPlaceName(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения индекса города из адреса, поиск
                        наименования города и запись последнего в `placeName`
    """

    if str(target.address) == "nan" or target.address is None:
        target.placeName = None
    else:
        if foundAddressIndex := re.findall(r"\d{6}", target.address):
            if basePostalCodes.get(foundAddressIndex[0]):
                target.placeName = basePostalCodes[
                    foundAddressIndex[0]]["placeCityName"]
            else:
                target.placeName = None
        else:
            target.placeName = None


@event.listens_for(LicensesMinCulture, "before_insert")
def setOrgContacts(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения 
                        ИНН компании и внесение контактов организации
    """

    if str(target.inn) == "nan" or target.address is None:
        target.inn = None
    else:
        if baseOrgsContacts.get(target.inn):
            target.contactPhone  = baseOrgsContacts[target.inn]["contactPhone"]
            target.contactEmail  = baseOrgsContacts[target.inn]["contactEmail"]
            target.contactPerson = baseOrgsContacts[target.inn]["contactPerson"]
        else:
            target.contactPhone  = None
            target.contactEmail  = None
            target.contactPerson = None


def updateModelsStorage(dbConnection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в БД
    """

    Base.metadata.create_all(dbConnection)

    return 0
