from _modules.servicesFiles.ProcessFileXml import ProcessFileXml


class ContractProjectSigned:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка файлов с информацией о подписанном контракте
    """

    def __init__(self, ramFileBuffer: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса
                        по обработке файла с информацией о подписанном контракте
        """

        self.processedFile = ProcessFileXml(ramFileBuffer)

        self.dataStructure = {

            "contractNum": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractSign/commonInfo/number"],
                },
                "data": ""
            },

            "contractTsm": {
                "extractionParams": {
                    "multi": False,
                    "xPath": ["cpContractSign/commonInfo/publishDTInEIS"],
                },
                "data": ""
            },

        }
        
    def extractionData(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
        """

        for i in self.dataStructure.keys():
            self.dataStructure[i]["data"] = self.processedFile.essenceDataWithPaths(
                self.dataStructure[i]["extractionParams"]["xPath"], 
                multi = self.dataStructure[i]["extractionParams"]["multi"]
            )
        
        print(self.dataStructure)
