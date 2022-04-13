from sqlalchemy import false
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

        self.processedFile = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProjectChange/commonInfo/number"],
                },
                "data": ""
            },

            "contractTsm": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProjectChange/commonInfo/publishDTInEIS"],
                },
                "data": ""
            },

            "acceptedAll": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractProjectChange/changeInfo/totallyAccepted"],
                },
                "data": False
            },

        }
        
    def extractionData(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
        """

        for i in self.dataStructure.keys():
            self.processedFile.essenceDataWithPaths(
                self.dataStructure[i]["extractionParams"]["xPath"], 
                multi = self.dataStructure[i]["extractionParams"]["multi"]
            )
