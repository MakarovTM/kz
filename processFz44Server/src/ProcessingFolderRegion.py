from _db.DbConnection import DbConnection

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
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

        self._config = ProgramConfig()
        self._logger = ProgramLogger()

        self._dbConnection = DbConnection("kzRemoteDataBase")

        self._serverConnection = ServerViaFTP(
            self._config.config["zakupkiGovServer"]["host"],
            self._config.config["zakupkiGovServer"]["port"],
            self._config.config["zakupkiGovServer"]["user"],
            self._config.config["zakupkiGovServer"]["pasw"]
        )

    def __processFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки директории
        """

        if self._serverConnection.\
                changeProcessPath(self._processingServerPath) == 0:
            for toProcessFile in self._serverConnection.browseProcessPath():
                if self.__processFolderFile(toProcessFile) == 0:
                    self._logger.logInfo(
                        f"Запуск процесса обработки файла {toProcessFile}"
                    )
                else:
                    self._logger.logError(
                        f"Обработка файла {toProcessFile} завершена с ошибкой"
                    )
        else:
            self._logger.logError(
                f"Ошибка при смене каталога {self._processingServerPath}"
            )

        return 0

    def __processFolderFile(self, toProcessFile: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла внутри директории
        """

        processingZipFile = ProcessFileZip(
            self._serverConnection.uploadFileInRam(toProcessFile)
        )

        for inZipFileName in processingZipFile.showStructureOfZip(".*.xml"):
            ProcessingFolderStrategics(
                inZipFileName,
                processingZipFile.readZipFileContent(inZipFileName)
            ).saveEssencedData()
            self._dbConnection.commitDbConnectionSession()

        return 0

    def runProcessFolderRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории с файлами
        """

        if self._serverConnection.createConnection() == 0:
            if self._dbConnection.createDbConnection() == 0:
                if self.__processFolder() == 0:
                    self._logger.logInfo(
                        f"""
                            Обработка каталога
                            {self._processingServerPath} завершена успешно
                        """
                    )

        return 0
