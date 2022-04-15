from _db.DbConnection import DbConnection
from _db.DbModelsStorage import ContractProjectProtocolChanged

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml


class ContractProjectChanged:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка файлов с изменениями проектов контрактов
    """

    def __init__(self, ramFileBuffer: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса
                        по обработке файла с изменениями проектов контрактов
        """

        self.dbConnection = DbConnection()
        self.xmlModelTree = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProjectChange/commonInfo/number",
                        "nested": None
                    },
                    "stand": "",
                    "shape": None
                },
                "data": ""
            },

            "contractTsm": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProjectChange/commonInfo/publishDTInEIS",
                        "nested": None
                    },
                    "stand": "1970-01-01 00:00:00",
                    "shape": "IsoDateFormatter"
                },
                "data": ""
            },

            "acceptedAll": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProjectChange/changeInfo/totallyAccepted",
                        "nested": None
                    },
                    "stand": "false",
                    "shape": "BoolIntFormatter"
                },
                "data": ""
            },

        }
        
    def extractionData(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
        """

        for i in self.dataStructure.keys():
            self.dataStructure[i]["data"] = self.xmlModelTree.essenceDataWithXpath(
                essenceStructure = self.dataStructure[i]["extractionParams"]
            )

        return 0

    def saveExtractedDataIntoDb(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        self.dbConnection.dbConSessionItems.append(
            ContractProjectProtocolChanged(
                **{i: self.dataStructure[i]["data"] for i in self.dataStructure.keys()}
            )
        )

        return 0
