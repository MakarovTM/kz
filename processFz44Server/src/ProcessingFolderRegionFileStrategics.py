import re

from io import BytesIO

from src.planGraphs.TenderPlan2020 import TenderPlan2020


class ProcessingFolderRegionFileStrategics:

    """
        Автор:          Макаров Алексей
        Описание:       Поведенческий паттерн, управляющий
                        процессом извлечения данных из XML файлов с закупками
    """

    def __init__(self, fileName: str, fileContent: BytesIO) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self._essenceDataTool = None

        if re.match(r"tenderPlan2020[_\d]+.xml", fileName):
            self._essenceDataTool = TenderPlan2020(fileContent)
