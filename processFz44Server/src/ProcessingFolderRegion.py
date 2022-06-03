from pymysql import DatabaseError
from tqdm import tqdm
from _db.DbConnection import DbConnection
from _db.modelStorage.ProcessingFileStatus import ProcessingFileStatus
from _vars.programReports import programReports

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
from _modules.servicesServer.ServerViaSSH import ServerViaSsh

from _modules.servicesFiles.ProcessFileZip import ProcessFileZip

from _modules.servicesProgram.ProgramLogger import ProgramLogger
from _modules.servicesProgram.ProgramConfig import ProgramConfig

from src.ProcessingFolderStrategics import ProcessingFolderStrategics


class ProcessingFolderRegion:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки директории с архивами ...
    """

    def __init__(self, processingServerPath: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self._processingServerPath = processingServerPath

        self._zrServerConnection = None
        self._kzServerConnection = None

        self._kzServerDbConnection = None

        self._config = ProgramConfig()
        self._logger = ProgramLogger()

        self.__createKzServerConnection()
        self.__createKzServerDbConnection()

        self.__createZrServerConnection()

    def __createKzServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с сервером vm20.trade.su
        """

        try:
            self._kzServerConnection = ServerViaSsh(

                host=self._config.config["vm20TradeSu"]["host"],
                port=self._config.config["vm20TradeSu"]["port"],
                user=self._config.config["vm20TradeSu"]["user"],
                pasw=self._config.config["vm20TradeSu"]["pasw"],

                dbHost=self._config.config["vm20TradeSu"]["dbHost"],
                dbPort=self._config.config["vm20TradeSu"]["dbPort"],

            )
            if self._kzServerConnection.createServerConnection() == 0:
                self._logger.logInfo(
                    programReports["info"]["serverConnectionEstablished"]
                )
            else:
                raise ConnectionError
        except ConnectionError:
            self._logger.logError(
                programReports["errors"]["serverConnectionError"]
            )
            return 1

        return 0

    def __createZrServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание;   Создание соединения с FTP - сервером закупок
        """

        try:
            self._zrServerConnection = ServerViaFTP(
                host=self._config.config["zakupkiGovServer"]["host"],
                port=self._config.config["zakupkiGovServer"]["port"],
                user=self._config.config["zakupkiGovServer"]["user"],
                pasw=self._config.config["zakupkiGovServer"]["pasw"],
            )
            if self._zrServerConnection.createConnection() == 0:
                self._logger.logInfo(
                    programReports["info"]["serverConnectionEstablished"]
                )
            else:
                raise ConnectionError
        except ConnectionError:
            self._logger.logError(
                programReports["errors"]["serverConnectionError"]
            )
            return 1

        return 0

    def __createKzServerDbConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение создания соединения
                        с локальной БД, расположенной на vm20TradeSu
        """

        try:
            if self._kzServerConnection is None:
                raise ConnectionError
            else:
                self._kzServerDbConnection = DbConnection(
                    dbHost=self._config.config["vm20TradeSuDb"]["host"],
                    dbPort=self._kzServerConnection.showLocalBindPort(),
                    dbUser=self._config.config["vm20TradeSuDb"]["user"],
                    dbName=self._config.config["vm20TradeSuDb"]["dbName"]
                )
                if self._kzServerDbConnection.createDbConnection() == 0:
                    self._logger.logInfo(
                        programReports["info"]["dbConnectionEstablished"]
                    )
                    self._kzServerDbConnection.updateDbModelStorage()
                else:
                    raise DatabaseError
        except DatabaseError:
            self._logger.logError(
                programReports["errors"]["dbConnectionError"]
            )
            return 1
        except ConnectionError:
            self._logger.logError(
                programReports["errors"]["serverConnectionError"]
            )
            return 1

        return 0

    def __processFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки директории
        """

        if self._zrServerConnection is not None:
            if self._zrServerConnection.changeProcessPath(
                self._processingServerPath
            ) == 0:
                for toProcessFileName in tqdm(self.\
                        _zrServerConnection.browseProcessPath()):
                    self.__processFolderFile(toProcessFileName)

        return 0

    def __processFolderFile(self, toProcessFileName: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла на сервере
        """

        processingZipInRam = ProcessFileZip(
            self._zrServerConnection.uploadFileInRam(
                toProcessFileName
            )
        )

        for toProcessFileInZip \
                in tqdm(processingZipInRam.showStructureOfZip(".*.xml")):
            processingFileInZipStrategics = ProcessingFolderStrategics(
                toProcessFileInZip,
                processingZipInRam.readZipFileContent(
                    toProcessFileInZip
                ),
                self._kzServerDbConnection
            )
            if processingFileInZipStrategics.checkProcessingStrategics():
                processingFileInZipStrategics.saveEssencedData()
                self._kzServerDbConnection.commitDbConnectionSession()

        return 0

    def runProcessFolderRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории с файлами
        """

        if self.__processFolder() == 0:
            self._logger.logInfo(
                f"""
                    Обработка каталога
                    {self._processingServerPath} завершена успешно
                """
            )

        return 0
