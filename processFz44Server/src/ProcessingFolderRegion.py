from pathlib import Path
from configparser import ConfigParser

from _db.DbConnection import DbConnection
from _db.modelStorage.ZakupkiFilesProcessingStatus import ZakupkiFilesProcessingStatus

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
from _modules.servicesFiles.ProcessFileZip import ProcessFileZip
from _modules.servicesProgram.ProgramLogger import ProgramLogger

from src.ProcessingFolderRegionFileStrategics import ProcessingFolderRegionFileStrategics


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

        self._config = ConfigParser()
        self._config.read(f"{Path(__file__).parents[1]}/config.ini")

        self._logger = ProgramLogger()

        self._dbConnection = DbConnection(
            self._config["kzRemoteDataBase"]["host"],
            self._config["kzRemoteDataBase"]["port"],
            self._config["kzRemoteDataBase"]["user"],
            self._config["kzRemoteDataBase"]["pasw"],
            self._config["kzRemoteDataBase"]["dbName"],
        )

        self._serverConnection = ServerViaFTP(
            self._config["zakupkiGovServer"]["host"],
            self._config["zakupkiGovServer"]["port"],
            self._config["zakupkiGovServer"]["user"],
            self._config["zakupkiGovServer"]["pasw"]
        )

        self._processingServerPath = processingServerPath

    def __processFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки директории
        """

        if self._serverConnection.\
                changeProcessPath(self._processingServerPath) == 0:
            for toProcessFile in self._serverConnection.browseProcessPath():
                self.__processFolderFile(toProcessFile)

    def __processFolderFile(self, toProcessFile: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла внутри директории
        """

        processingZipFile = ProcessFileZip(
            self._serverConnection.uploadFileInRam(toProcessFile)
        )

        for i in processingZipFile.showStructureOfZip(".*.xml"):
            ProcessingFolderRegionFileStrategics(i, processingZipFile.readZipFileContent(i))

    def __processFolderFileFinished(self, toProcessFileId: int) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Сохранение отметки об успешно обработакнном файле
        """

        pass

    def runProcessFolderRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории с файлами
        """

        if self._serverConnection.createConnection() == 0:
            if self._dbConnection.createDbConnection() == 0:
                self.__processFolder()

        return 0
