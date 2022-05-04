from io import BytesIO

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml

from _db.DbConnection import DbConnection
from _db.modelStorage.PurchaseProtocolFinal import PurchaseProtocolFinal


class ProtocolFinal:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки файлов, содержащих
                        информацию о результате проведения закупочной процедуры
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
            "purchaseReasonAbandoned": {
                "multi": False,
                "xPath": {
                    "parent": "./*/protocolInfo/abandonedReason/code",
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
            self._processingFile.essenceDataWithXpath(
                self._essenceDataStructure
            )
        )

    def saveEssencedDataToDb(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        for purchaseProtocolData in self.\
                _processingFile.essenceDataWithXpath(self._dataStructure):
            self._dbConnection.dbConnectionSession.add(
                PurchaseProtocolFinal(**purchaseProtocolData)
            )
