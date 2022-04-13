from _modules.servicesFiles.ProcessFileXml import ProcessFileXml
from _db.DbConnection import DbConnection
from _db.DbModelsStorage import ContractProjectsPublished


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
        self.processedFile = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/commonInfo/number"],
                    "shape": None
                },
                "data": ""
            },

            "contractPub": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/commonInfo/publishDTInEIS"],
                    "shape": "IsoDateFormatter"
                },
                "data": ""
            },

            "contractObj": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/contractInfo/subject"],
                    "shape": None
                },
                "data": ""
            },

            "contractPrc": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/contractInfo/price"],
                    "shape": None
                },
                "data": ""
            },

            "customerInn": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/customerInfo/INN"],
                    "shape": None
                },
                "data": ""
            },

            "supplierInn": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProject/participantInfo/*/INN"],
                    "shape": None
                },
                "data": ""
            }

        }
        
    def extractionData(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
        """

        for i in self.dataStructure.keys():
            self.dataStructure[i]["data"] = self.processedFile.essenceDataWithPaths(
                self.dataStructure[i]["extractionParams"]["xPath"], 
                multi = self.dataStructure[i]["extractionParams"]["multi"],
                shape = self.dataStructure[i]["extractionParams"]["shape"]
            )
        
        self.dbConnection.dbConSessionItems.append(
            ContractProjectsPublished(
                **{i: self.dataStructure[i]["data"] for i in self.dataStructure.keys()}
            )
        )