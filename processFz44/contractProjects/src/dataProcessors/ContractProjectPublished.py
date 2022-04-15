from _db.DbConnection import DbConnection
from _db.DbModelsStorage import ContractProjectsProtocolPublished

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml


class ContractProjectPublished:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка проекта контракта
    """

    def __init__(self, ramFileBuffer: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса
                        по обработке файла с проектом контракта
        """

        self.dbConnection = DbConnection()
        self.xmlModelTree = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/commonInfo/number",
                        "nested": None
                    },
                    "stand": "",
                    "shape": None
                },
                "data": ""
            },

            "contractPub": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/commonInfo/publishDTInEIS",
                        "nested": None
                    },
                    "stand": "1970-01-01 00:00:00",
                    "shape": "IsoDateFormatter"
                },
                "data": ""
            },

            "contractObj": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/contractInfo/subject",
                        "nested": None
                    },
                    "stand": "",
                    "shape": None
                },
                "data": ""
            },

            "contractPrc": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/contractInfo/price",
                        "nested": None
                    },
                    "stand": "0.00",
                    "shape": "FloatP2Formatter"
                },
                "data": ""
            },

            "customerInn": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/customerInfo/INN",
                        "nested": None
                    },
                    "stand": "",
                    "shape": None
                },
                "data": ""
            },

            "supplierInn": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpContractProject/participantInfo/*/INN",
                        "nested": None
                    },
                    "stand": "",
                    "shape": None
                },
                "data": ""
            }

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
            ContractProjectsProtocolPublished(
                **{i: self.dataStructure[i]["data"] for i in self.dataStructure.keys()}
            )
        )

        return 0
