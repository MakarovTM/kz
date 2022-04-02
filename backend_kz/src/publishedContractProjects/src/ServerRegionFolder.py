import datetime

from tqdm import tqdm

from modules.services_server.FTP_Server import FTP_Server

from src.publishedContractProjects.src.ServerRegionFolderZip import ServerRegionFolderZip

class ServerRegionFolder:

    """
        Автор:          Макаров Алексей
        Описание:       Выполенение обработки директории,
                        содержащей архивы с информацией о процедуре заключения контракта
    """

    def __init__(self, processingRegion: str) -> None:
    
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке директории на сервере
        """

        self.processingRegion = processingRegion
        self.currentTimeStamp = datetime.datetime.now()
        self.serverConnection = FTP_Server("ftp.zakupki.gov.ru", "free", "free")
    
    def __serverPathToProcess(self) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Определение пути к директории,
                        для которой выполняется обработка файлов
        """

        if self.currentTimeStamp.strftime("%d") == "1":
            return f"/fcs_regions/{self.processingRegion}/contractprojects/prevMonth"

        return f"/fcs_regions/{self.processingRegion}/contractprojects/prevMonth"

    def __changeServerPathToProcess(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Смена активной директории на сервере
        """

        if self.serverConnection.change_server_folder(self.__serverPathToProcess()) != 0:
            return 1

        return 0

    def __filterServerFilesToProcess(self, filterString = None) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Фильтрация файлов на сервере для последующей обработки
        """

        if filterString is not None:
            return self.serverConnection.listing_server_folder(filter_string = filterString)

        return self.serverConnection.listing_server_folder()

    def runServerRegionFolderProcessing(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории с проектами контрактов
        """

        if self.__changeServerPathToProcess() == 0:
            for i in self.__filterServerFilesToProcess():
                ServerRegionFolderZip(
                    self.serverConnection.upload_server_file_in_ram(i)
                ).updateContractProjectsTimeLine()

        return 0