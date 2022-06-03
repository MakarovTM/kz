from io import BytesIO

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml

from _db.modelStorage.UnscheduledChecks import UnscheduledChecks


class UnplannedCheck:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки файлов, содержащих
                        информацию о запланированных процедурах проведения
    """

    def __init__(self, ramFileBuffer: BytesIO, dbConnection) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self._dbConnection = dbConnection

        self._processingFile = ProcessFileXml(ramFileBuffer)

        self._dataStructure = {
            "config": {
                "stacked": False,
                "stackedRoot": None
            },
            "regNumber": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/regNumber",
                    "nested": None
                }
            },
            "ispectorInn": {
                "multi": False,
                "xPath": {
                    "parent": "./*/inspector/INN",
                    "nested": None
                }
            },
            "ispectorName": {
                "multi": False,
                "xPath": {
                    "parent": "./*/inspector/fullName",
                    "nested": None
                }
            },
            "inspectedInn": {
                "multi": False,
                "xPath": {
                    "parent": "./*/checkedSubject/customer/INN",
                    "nested": None
                }
            },
            "inspectedName": {
                "multi": False,
                "xPath": {
                    "parent": "./*/checkedSubject/customer/fullName",
                    "nested": None
                }
            },
            "noticeDescription": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/notice/info",
                    "nested": None
                }
            },
            "inspectionPlannedDate": {
                "multi": False,
                "xPath": {
                    "parent": "./*/inspectionDate",
                    "nested": None
                }
            },
            "inspectionPublishedDate": {
                "multi": False,
                "xPath": {
                    "parent": "./*/commonInfo/publishDate",
                    "nested": None
                }
            },
            "printFormUrl": {
                "multi": False,
                "xPath": {
                    "parent": "./*/printForm/url",
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
                self._dataStructure
            )
        )

    def saveEssencedDataToDb(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        for unplannedCheckData in self.\
                _processingFile.essenceDataWithXpath(self._dataStructure):

            dbRow = self._dbConnection.dbConnectionSession.\
                    query(UnscheduledChecks).\
                    filter_by(regNumber=unplannedCheckData["regNumber"]).\
                    first()

            if dbRow is not None:
                self._dbConnection.dbConnectionSession.\
                    query(UnscheduledChecks).\
                    filter(UnscheduledChecks.id == dbRow.id).\
                    update(unplannedCheckData)
            else:
                self._dbConnection.\
                    dbConnectionSession.add(
                        UnscheduledChecks(**unplannedCheckData))
