import io
import os
import re
import pandas
import requests

from tqdm import tqdm
from pathlib import Path
from configparser import ConfigParser

from _db.dbConnection import dbConnection
from _db.dbModelsStorage import LicensesMinCulture

from _modules.Logger import Logger
from _modules.ServerViaSsh import ServerViaSsh

from src.licenseMinCulture.vars.columnNames import columnNames


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

        self._rootPath = Path(__file__).parents[2]
        self._dataExtracted = list()

        self._logger = Logger()
        self._config = ConfigParser()
        
    def __readConfigFile(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение чтения конфигурационного файла
        """
    
        try:
            self._config.read(f"{self._rootPath}/config.ini")
        except Exception as e:
            self._logger.logCritError(
                f"Произошла ошибка при чтении конфигурационного файла - {str(e)}"
            )

        return 0

    def __createDbServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения 
                        с сервером, на котором расположена БД
        """

        self._dbServerConnection = ServerViaSsh(

            self._config["vm20TradeServer"]["host"],
            self._config["vm20TradeServer"]["port"],

            self._config["vm20TradeServer"]["user"],
            self._config["vm20TradeServer"]["pasw"],

            self._config["vm20TradeServerDb"]["dbHost"],
            self._config["vm20TradeServerDb"]["dbPort"],

        )

        return 0 if self._dbServerConnection.createConnection() == 0 else 1

    def __createDbOnServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения
                        с базой данных, расположенной на подключенном сервере
        """

        self._dbOnServerConnection = dbConnection(

            self._config["vm20TradeServerLocalDb"]["dbHost"],
            self._dbServerConnection.serverConnection.local_bind_port,
            self._config["vm20TradeServerLocalDb"]["dbUser"],

        )

        self._dbOnServerConnection.createConnection()

        return 0 if self._dbOnServerConnection.createConnectionSession() == 0 else 1

    def __processingFileCheckVersion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение проверки 
                        версии выложенного файла для парсинга данных
        """

        try:
            response = requests.get(self._config["licenseMinCulture"]["url"])
            if response.status_code == 200:
                self._publishedDataSet = re.findall(
                    self._config["licenseMinCulture"]["reg"], response.text
                )
            else:
                return 1
        except Exception as e:
            self._logger.logCritError(
                f"Ошибка при проверке версии файла с лицензиями мин. культуры - {str(e)}"
            )

        return 0 if self._config["licenseMinCulture"]["ver"] != self._publishedDataSet[0][1] else 1

    def __processingFileInload(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение загрузки файла 
                        с информацией о выданных лицензиях
        """

        try:
            response = requests.get(
                f"{self._config['licenseMinCulture']['url']}/{self._publishedDataSet[0][0]}.csv"
            )
            if response.status_code == 200:
                self._inloadedFile = response.text
            else:
                return 1
        except Exception as e:
            self._logger.logCritError(
                f"Ошибка при попытке загрузки файла с лицензиями мин культуры - {str(e)}"
            )
        
        return 0

    def __processingFileProduction(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения 
                        и сохранения данных в БД из загруженного файла
        """

        licensesDf = pandas.read_csv(io.StringIO(self._inloadedFile), dtype = str)

        try:
            for licenseRow in licensesDf[
                [i["csvColumnName"] for i in columnNames]].values.tolist():
                    self._dataExtracted.append(
                        {
                            columnNames[columnIndex]["sqlColumnName"]: columnData
                            for columnIndex, columnData in enumerate(licenseRow)
                        }
                    )
        except Exception as e:
            self._logger.logCritError(
                f"Произошла ошибка при извлечении данных из загруженного файла - {str(e)}"
            )

        return 0

    def __exportDataToDb(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения извлеченных данных в БД
        """

        for dataRow in tqdm(self._dataExtracted[:50]):
            dbRow = self._dbOnServerConnection.dbConnectionSession.query(LicensesMinCulture).filter_by(licenseId = dataRow["licenseId"]).first()
            if dbRow is None:
                self.\
                    _dbOnServerConnection.\
                        dbConnectionSession.\
                            add(LicensesMinCulture(**dataRow))
            else:
                self.\
                    _dbOnServerConnection.\
                        dbConnectionSession.\
                            query(LicensesMinCulture).\
                                filter(LicensesMinCulture.id == dbRow.id).\
                                    update(**dataRow)

        return 0

    def runDataParsing(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса парсинга
                        данных о лицензиях, выданных Министерством культуры
        """

        if self.__readConfigFile() == 0:
            if self.__createDbServerConnection() == 0:
                if self.__createDbOnServerConnection() == 0:
                    self._dbOnServerConnection.updateModelsStorage()
                    if self.__processingFileCheckVersion() == 0:
                       if self.__processingFileInload() == 0:
                           self.__processingFileProduction()
                           self.__exportDataToDb()
        self._dbOnServerConnection.commitSession()


            # self.__updateLicensesFileVersion()
