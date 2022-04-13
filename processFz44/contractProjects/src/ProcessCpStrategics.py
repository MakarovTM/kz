import re

from contractProjects.src.dataProcessors.ContractProjectSigned import ContractProjectSigned
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

        """if re.match(r"cpContractProjectChange[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectChanged(contractProjectContent)

        if re.match(r"cpContractSign[_\d]+.xml", contractProjectFileName):
            self.extractionTool = ContractProjectSigned(contractProjectContent)"""

    def processData(self):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки данных
        """
        
        if self.extractionTool is not None:
            self.extractionTool.extractionData()
