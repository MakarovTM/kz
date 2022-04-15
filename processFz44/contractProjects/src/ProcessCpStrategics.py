import re

from contractProjects.src.dataProcessors.ContractProjectSigned import ContractProjectSigned
from contractProjects.src.dataProcessors.ContractProjectCancel import ContractProjectCancel
from contractProjects.src.dataProcessors.ContractProjectChanged import ContractProjectChanged
from contractProjects.src.dataProcessors.ContractProjectPublished import ContractProjectPublished


class ProcessCpStrategics:

    """
        Автор:          Макаров Алексей
        Описание:       Поведенческий паттерн,
                        управляющий процессом извлечения данных проектов контрактов 
    """

    def __init__(self, contractProjectContent: bytes, contractProjectFileName: str) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса
        """

        self.extractionTool = None

        if re.match(r"cpContractProject[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectPublished(contractProjectContent)

        if re.match(r"cpContractProjectChange[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectChanged(contractProjectContent)

        if re.match(r"cpContractSign[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectSigned(contractProjectContent)
        
        if re.match(r"cpProcedureCancel[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectCancel(contractProjectContent)

    def showDataExtracted(self):

        """
            Автор:      Макаров Алексей
            Описание:   Извлечение и вывод данных в консоль
        """

        if self.extractionTool is not None:
            if self.extractionTool.extractionData() == 0:
                print(self.extractionTool.dataStructure)

    def saveDataExtracted(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Сохранение извлеченных данных в БД
        """
        
        if self.extractionTool is not None:
            if self.extractionTool.extractionData() == 0:
                self.extractionTool.saveExtractedDataIntoDb()
