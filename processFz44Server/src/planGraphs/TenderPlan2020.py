from io import BytesIO

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml

from _db.DbConnection import DbConnection


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

        self._processingFile = ProcessFileXml(ramFileBuffer)

        self._essenceDataStructure = {
            "config": {
                "stacked": True,
                "stackedRoot": "tenderPlan2020/positions",
            },
            "ikz": {
                "multi": False,
                "xPath": {
                    "parent": "commonInfo/IKZ",
                    "nested": None
                }
            },
            "okv": {
                "multi": True,
                "xPath": {
                    "parent": "commonInfo/OKPD2Info",
                    "nested": "OKPDCode"
                }
            }
        }

        print(
            self._processingFile.essenceDataWithXpath(self._essenceDataStructure)
        )
