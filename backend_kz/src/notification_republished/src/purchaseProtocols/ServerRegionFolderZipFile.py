from db.DB_Connection import DB_Connection
from db.DB_ModelsStorage import RepublishedNotifications

from modules.services_files.XML_Process import XML_Process


class ServerRegionFolderZipFile:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения 
                        данных из файла с информацией о закупке
    """

    def __init__(self, purchase_file_content: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса 
                        по извлечению данных о закупке из файла
        """

        self.dbConnection = DB_Connection()
        self.purchase_file_content = XML_Process(purchase_file_content)

    def essenceData(self):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
        """
            
        num = self.purchase_file_content.essenceDataWithPaths(
            ["*/commonInfo/purchaseNumber"], multi = False
        )

        fcd = self.purchase_file_content.essenceDataWithPaths(
            ["*/protocolInfo/abandonedReason/code"], multi = False
        )

        print(num, fcd)
