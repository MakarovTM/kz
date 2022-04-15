import asyncio
import datetime

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

        self.loop = asyncio.get_event_loop()

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

    async def __processFolderFile(self, toProcessFolderFile: str):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла на FTP сервере
        """

        a = self.serverConnection.inloadFolderFile(toProcessFolderFile)
        _ = ProcessFileZip(a)
        for i in _.zipFileShowStructure():
            ProcessCpStrategics(_.readFilesIntoArchive(i), i).saveDataExtracted()

        await asyncio.sleep(0.1)

    async def __processFolder(self, toProcessFolder: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории
        """

        tasks = []

        if self.serverConnection.changeWorkFolder(toProcessFolder) == 0:
            for i in self.serverConnection.viewOpenedFolder():
                tasks.append(self.__processFolderFile(i))
        await asyncio.gather(*tasks)

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение процесса обработки файлов на сервере 
        """

        for processPath in tqdm(self.__processingPaths()):
            asyncio.run(self.__processFolder(processPath))
            self.dbConnection.commitSession()

        return 0
