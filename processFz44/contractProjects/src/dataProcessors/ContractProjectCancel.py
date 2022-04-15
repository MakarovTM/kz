from _db.DbConnection import DbConnection
from _db.DbModelsStorage import ContractProjectProtocolCancel

from _modules.servicesFiles.ProcessFileXml import ProcessFileXml


class ContractProjectCancel:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка файлов с 
                        информацией об отмене процедуры заключения контракта
    """

    def __init__(self, ramFileBuffer: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке файла 
                        с информацией об отмене процедуры заключения контракта
        """

        self.dbConnection = DbConnection()
        self.xmlModelTree = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": None,
                    "xPath": {
                        "parent": "cpProcedureCancel/commonInfo/number",
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
                        "parent": "cpProcedureCancel/commonInfo/publishDTInEIS",
                        "nested": None
                    },
                    "stand": "1970-01-01 00:00:00",
                    "shape": "IsoDateFormatter"
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
            ContractProjectProtocolCancel(
                **{i: self.dataStructure[i]["data"] for i in self.dataStructure.keys()}
            )
        )

        return 0
    