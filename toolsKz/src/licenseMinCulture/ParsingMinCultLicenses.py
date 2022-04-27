import os
from pickle import NONE
import re
import io
import sys
import requests
import pandas as pd
import configparser
import threading

from tqdm import tqdm
from _db.dbConnection import dbConnection
from _db.dbModelsStorage import LicensesMinCulture

from _modules.ServerViaSsh import ServerViaSsh


class ParsingMinCultLicenses:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение парсинга
                        данных о лицензиях Министерства культуры
    """

    def __init__(self) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self.iniConfigFile = configparser.ConfigParser()
        self.iniConfigFile.read(f"{os.path.dirname(__file__)}/settings.ini")

        self.serverConnection = ServerViaSsh(
            self.iniConfigFile["sshServer"]["host"], self.iniConfigFile["sshServer"]["port"],
            self.iniConfigFile["sshServer"]["user"], self.iniConfigFile["sshServer"]["pasw"],
            self.iniConfigFile["sshServer"]["dbHost"], self.iniConfigFile["sshServer"]["dbPort"],
        )
        self.serverConnection.createConnection()

        self.dbConnection = dbConnection(
            "localhost",
            self.serverConnection.serverConnection.local_bind_port,
            "rosexport"
        )

        self.dbConnection.createConnection()
        self.dbConnection.createConnectionSession()

        self.dbConnection.updateModelsStorage()
        

    def __checkFileLoadVersion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение проверки 
                        версии выложенного файла для парсинга данных
        """

        response = requests.get(self.iniConfigFile["default"]["sourceUrl"])
        
        if response.status_code == 200:
            if foundDataSetVer := re.findall(
                self.iniConfigFile["default"]["reDataSetVer"], response.text
            ):
                if foundDataSetVer[0][1] == self.iniConfigFile["default"]["datasetVer"]:
                    print("Значение не изменилось")
                    return 1
                else:
                    self.foundDataSetVer = foundDataSetVer
            else:
                print("Значение не найдено")
                return 1
        else:
            print(f"Ошибка выполнения запроса - {response.status_code}")
            return 1

        return 0

    def __inloadLicensesFile(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение загрузки файла 
                        с информацией о выданных лицензиях
        """

        response = requests.get(f"{self.iniConfigFile['default']['sourceUrl']}/{self.foundDataSetVer[0][0]}.csv")

        return pd.read_csv(io.StringIO(response.text), dtype = str)[["Полное наименование", "ИНН", "OГРН/ОГРНИП", "Дата регистрации лицензии", "Дата прекращения действия лицензии", "Номер лицензии"]].values.tolist()

    def __saveСompanyLicenseDataRow(self, companyLicenseData: list):

        row = self.dbConnection.dbConnectionSession.query(LicensesMinCulture).filter_by(orgInn = companyLicenseData[1]).first()

        if row is not None:
            self.dbConnection.dbConnectionSession.query(LicensesMinCulture).\
                filter(LicensesMinCulture.id == row.id).\
                    update({
                        "orgName": companyLicenseData[0],
                        "orgInn": companyLicenseData[1],
                        "orgOgrn": companyLicenseData[2],
                        "licenseFrom": companyLicenseData[3],
                        "licenseTill": companyLicenseData[4],
                        "licenseNumber": companyLicenseData[5],
                    })
        else:
            self.dbConnection.dbConnectionSession.add(LicensesMinCulture(
                orgName = companyLicenseData[0],
                orgInn = companyLicenseData[1],
                orgOgrn = companyLicenseData[2],
                licenseFrom = companyLicenseData[3],
                licenseTill = companyLicenseData[4],
                licenseNumber = companyLicenseData[5],
            ))

    def __updateLicensesFileVersion(self):

        self.iniConfigFile["default"]["datasetVer"] = self.foundDataSetVer[0][1]

        with open(f"{os.path.dirname(__file__)}/settings.ini", "w") as configfile:
            self.iniConfigFile.write(configfile)

    def runDataParsing(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса парсинга
                        данных о лицензиях, выданных Министерством культуры
        """


        if self.__checkFileLoadVersion() == 0:

            for i in tqdm(self.__inloadLicensesFile()):
                try:
                    self.__saveСompanyLicenseDataRow(i)
                except Exception as e:
                    pass

            try:
                self.dbConnection.commitSession()
            except Exception as e:
                print(e)
                pass
            self.serverConnection.deleteConnection()

            # self.__updateLicensesFileVersion()
