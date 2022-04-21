import threading

from _vars.processingRegions import fz44ProcessingRegions

from contractProjects.src.ContractProjectsProcessRegion import ContractProjectsProcessRegion


class ContractProjects:

    """
        Автор:          Макаров Алексей
        Описание:       Обработка директории 
                        с проектами контрактов на сервере ftp.zakupki.gov.ru
    """

    def __init__(self) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        self.toProcessRegions = fz44ProcessingRegions
    
    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение процесса обработки файлов на сервере
        """

        for i in self.toProcessRegions:
            ContractProjectsProcessRegion(i).processRegionRun()
            break
