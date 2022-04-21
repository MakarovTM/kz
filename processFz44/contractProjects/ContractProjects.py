import datetime
import threading
import time

from tqdm import tqdm

from _db.DbConnection import DbConnection

from _vars.processingRegions import fz44ProcessingRegions

from _modules.servicesServers.ServerViaFTP import ServerViaFTP
from _modules.servicesFiles.ProcessFileZip import ProcessFileZip

from contractProjects.src.ProcessCpStrategics import ProcessCpStrategics


class ContractProjects:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка директории 
                        с проектами контрактов на сервере ftp.zakupki.gov.ru
    """

    def __init__(self) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке директории
        """

        self.dbConnection = DbConnection()
        self.currentTimeStamp = datetime.datetime.now()
        self.toProcessRegions = fz44ProcessingRegions
        self.serverConnection = ServerViaFTP("ftp.zakupki.gov.ru", "free", "free")

        if self.serverConnection.createConnection() != 0:
            print("Ошибка создания соединения с FTP сервером")
            raise ConnectionError

    def __processingPaths(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Создание пути на сервере для обработки файлов
        """

        folderName = "prevMonth" if self.currentTimeStamp.strftime("%d") == 1 else "currMonth"

        return [
            f"/fcs_regions/{region}/contractprojects/{folderName}/" 
            for region in self.toProcessRegions
        ]

    def __processFolderFile(self, toProcessFolderFile: str):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла на FTP сервере
        """

        a = self.serverConnection.inloadFolderFile(toProcessFolderFile)
        _ = ProcessFileZip(a)
        for i in _.zipFileShowStructure():
            ProcessCpStrategics(_.readFilesIntoArchive(i), i).saveDataExtracted()

    def __processFolder(self, toProcessFolder: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории
        """

        server = ServerViaFTP("ftp.zakupki.gov.ru", "free", "free")

        if self.serverConnection.changeWorkFolder(toProcessFolder) == 0:
            for i in self.serverConnection.viewOpenedFolder():
                self.__processFolderFile(i)

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение процесса обработки файлов на сервере 
        """

        for processPath in tqdm(self.__processingPaths()):
            self.__processFolder(processPath)
            self.dbConnection.commitSession()

        return 0
