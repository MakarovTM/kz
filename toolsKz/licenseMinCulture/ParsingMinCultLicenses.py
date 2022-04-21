import os
import re
import requests
import pandas as pd
import configparser

from _db.dbConnection import dbConnection
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
        self.dbConnection.deleteConnection()

        self.serverConnection.deleteConnection()

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

        licensesData = pd.read_excel(f"{self.iniConfigFile['default']['sourceUrl']}/{self.foundDataSetVer[0][0]}.xlsx")
        print(licensesData)

    def runDataParsing(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса парсинга
                        данных о лицензиях, выданных Министерством культуры
        """

        if self.__checkFileLoadVersion() == 0:

            self.__inloadLicensesFile()
