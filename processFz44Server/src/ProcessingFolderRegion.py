from pathlib import Path
from configparser import ConfigParser

from _db.DbConnection import DbConnection
from _db.modelStorage.ZakupkiFilesProcessingStatus import ZakupkiFilesProcessingStatus

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
from _modules.servicesProgram.ProgramLogger import ProgramLogger


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

    def __toProcessFilesList(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Получение списка файлов для последующей обработки
        """

        return []

    def runProcessFolderRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории с файлами
        """

        return 0
