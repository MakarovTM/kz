import datetime

from modules.services_server.FTP_Server import FTP_Server

from src.notification_prepaid.src.ServerRegionFolderZip import ServerRegionFolderZip


class ServerRegionFolder:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки директории,
                        содержащей файлы с информацией о предстоящей закупке
    """

    def __init__(self, process_region_name: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке директории
        """

        self.server_connection = None
        self.processing_region = process_region_name
        self.current_timestamp = datetime.datetime.now()

    def __to_process_server_path(self, to_process_region_name: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Определяем путь к директории, 
                        для которой выполняется обработка файлов
        """

        if self.current_timestamp.strftime("%d") == "1":
            return f"/fcs_regions/{self.processing_region}/notifications/prevMonth/"
        else:
            return f"/fcs_regions/{self.processing_region}/notifications/currMonth/"

    def make_server_connection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с сервером zakupki.gov.ru 
        """

        self.server_connection = FTP_Server("ftp.zakupki.gov.ru", "free", "free")

        if self.server_connection is not None:
            if self.server_connection.change_server_folder(self.__to_process_server_path(self.processing_region)) == 0:
                for i in self.server_connection.listing_server_folder(filter_string = self.current_timestamp.strftime("%Y%m%d")):
                    return ServerRegionFolderZip(i, self.server_connection).run_zip_processing()

        return 0
