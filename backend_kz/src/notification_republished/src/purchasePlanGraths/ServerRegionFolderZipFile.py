from db.DB_Connection import DB_Connection
from db.DB_Models import RepublishedNotifications

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

        for elem in self.purchase_file_content.createNewRootIterator("{http://zakupki.gov.ru/oos/TPtypes/1}position"):
            
            ikz = (
                self.purchase_file_content.essenceDataWithNeighbours(
                    "commonInfo", "IKZ", elem
                )
            )

            okv = (
                self.purchase_file_content.essenceDataWithNeighbours(
                    "OKPD2Info", "OKPDCode", elem
                )
            )

            obj = (
                self.purchase_file_content.essenceDataWithNeighbours(
                    "commonInfo", "purchaseObjectInfo", elem
                )
            )

            prc = (
                self.purchase_file_content.essenceDataWithNeighbours(
                    "financeInfo", "total", elem
                )
            )

            self.dbConnection.addObjectToSession(
                RepublishedNotifications(
                    ikz = ikz, obj = obj, okv = okv, prc = prc, crn = ikz[3:13]
                )
            )
