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

        for elem in self.purchase_file_content.createNewRootIterator("position"):
            
            ikz = self.purchase_file_content.essenceDataWithPaths(
                ["commonInfo/IKZ"], multi = False, element = elem
            )

            okv = self.purchase_file_content.essenceDataWithPaths(
                [
                    "OKPD2Info",
                    "OKPDCode"
                ], multi = True, element = elem
            )

            obj = self.purchase_file_content.essenceDataWithPaths(
                ["commonInfo/purchaseObjectInfo"], multi = False, element = elem
            )

            prc = self.purchase_file_content.essenceDataWithPaths(
                ["financeInfo/total"], multi = False, element = elem
            )

            mrs = self.purchase_file_content.essenceDataWithPaths(
                ["commonInfo/positionModification/changeReason/name"], multi = False, element = elem
            )

            self.dbConnection.dbConSessionItems.append(
                RepublishedNotifications(
                    ikz = ikz, okv = okv, obj = obj, prc = prc, crn = ikz[4:13], mrs = mrs
                )
            )
        
        self.dbConnection.commitSession()
