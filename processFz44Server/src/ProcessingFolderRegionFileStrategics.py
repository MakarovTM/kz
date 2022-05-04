import re

from io import BytesIO

from src.protocols.ProtocolFinal import ProtocolFinal
from src.planGraphs.TenderPlan2020 import TenderPlan2020
from src.notifications.EpNotification import EpNotification


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

        self._fileName = fileName
        self._essenceDataTool = None

        if re.match(r"epNotificationE.*.xml", fileName):
            self._essenceDataTool = EpNotification(fileContent)

        if re.match(r"epProtocol.*Final.*.xml", fileName):
            self._essenceDataTool = ProtocolFinal(fileContent)

    def showEssencedData(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения
                        данных по заданной структуре
        """

        if self._essenceDataTool is not None:
            self._essenceDataTool.showEssencedData()
        else:
            print("Просмотр данных невозможен, тк не был указан инструмент извлечения")
            print(self._fileName)

    def saveEssencedData(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения
                        извлеченных данных по заданной структуре
        """

        if self._essenceDataTool is not None:
            self._essenceDataTool.saveEssencedDataToDb()
