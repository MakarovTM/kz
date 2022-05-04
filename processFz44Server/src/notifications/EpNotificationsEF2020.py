from io import BytesIO

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml

from _db.DbConnection import DbConnection
from _db.modelStorage.PurchaseNotifications import PurchaseNotifications


class EpNotificationsEF2020:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки файлов, содержащих
                        информацию о планировании проведения процедур закупок
    """

    def __init__(self, ramFileBuffer: BytesIO) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self._dbConnection = DbConnection("kzRemoteDataBase")
        self._processingFile = ProcessFileXml(ramFileBuffer)

        self._dataStructure = {
            "config": {
                "stacked": False,
                "stackedRoot": None
            },
            "purchaseNum": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/purchaseNumber",
                    "nested": None
                }
            },
            "publishedEIS": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/publishDTInEIS",
                    "nested": None
                }
            },
            "purchaseObj": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/purchaseObjectInfo",
                    "nested": None
                }
            },
            "purchasePrc": {
                "multi": False,
                "xPath": {
                    "parent": "./*/*/*/maxPriceInfo/maxPrice",
                    "nested": None
                }
            },
            "placingFrom": {
                "multi": False,
                "xPath": {
                    "parent": "./*/*/procedureInfo/collectingInfo/startDT",
                    "nested": None
                }
            },
            "placingTill": {
                "multi": False,
                "xPath": {
                    "parent": "./*/*/procedureInfo/collectingInfo/endDT",
                    "nested": None
                }
            },
            "purchaseIkz": {
                "multi": False,
                "xPath": {
                    "parent": "./*/*/*/*/*/IKZInfo/purchaseCode",
                    "nested": None
                }
            },
        }

    def showEssencedData(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Просмотр извлеченных данных
        """

        print(
            self._processingFile.essenceDataWithXpath(self._dataStructure)
        )

    def saveEssencedDataToDb(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Сохранение извлеченных данных
        """

        for epNotificationData in self.\
                _processingFile.essenceDataWithXpath(self._dataStructure):

            dbRow = self._dbConnection.dbConnectionSession.\
                    query(PurchaseNotifications).\
                    filter_by(purchaseNum=epNotificationData["purchaseNum"]).\
                    first()

            if dbRow is not None:
                self._dbConnection.dbConnectionSession.\
                    query(PurchaseNotifications).\
                    filter(PurchaseNotifications.id == dbRow.id).\
                    update(epNotificationData)
            else:
                self._dbConnection.\
                    dbConnectionSession.add(
                        PurchaseNotifications(**epNotificationData))
