from io import BytesIO

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml

from _db.DbConnection import DbConnection
from _db.modelStorage.PlanGraphs import PlanGraphs


class TenderPlan2020:

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

        self._essenceDataStructure = {
            "config": {
                "stacked": True,
                "stackedRoot": "./tenderPlan2020/positions/position",
            },
            "purchaseIkz": {
                "multi": False,
                "xPath": {
                    "parent": "./commonInfo/IKZ",
                    "nested": None
                }
            },
            "purchaseObj": {
                "multi": False,
                "xPath": {
                    "parent": "./commonInfo/purchaseObjectInfo",
                    "nested": None
                }
            },
            "purchasePrc": {
                "multi": False,
                "xPath": {
                    "parent": "./financeInfo/total",
                    "nested": None
                }
            }
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

        for newTenderPlanRow in self._processingFile.essenceDataWithXpath(self._essenceDataStructure):
            self._dbConnection.dbConnectionSession.add(
                PlanGraphs(**newTenderPlanRow)
            )
