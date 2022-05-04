import re

from io import BytesIO

from src.protocols.ProtocolsFinal import ProtocolsFinal
from src.notifications.EpNotificationsEF2020 import EpNotificationsEF2020

from _modules.servicesProgram.ProgramLogger import ProgramLogger


class ProcessingFolderStrategics:

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

        self._logger = ProgramLogger()

        if re.match(r"epNotificationE.*.xml", fileName):
            self._essenceDataTool = EpNotificationsEF2020(fileContent)

        if re.match(r"epProtocol.*Final.*.xml", fileName):
            self._essenceDataTool = ProtocolsFinal(fileContent)

    def showEssencedData(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения
                        данных по заданной структуре
        """

        if self._essenceDataTool is not None:
            self._essenceDataTool.showEssencedData()
        else:
            self._logger.logError(
                "Для обработки передан файл неизвестного формата"
            )

    def saveEssencedData(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения
                        извлеченных данных по заданной структуре
        """

        if self._essenceDataTool is not None:
            self._essenceDataTool.saveEssencedDataToDb()
        else:
            self._logger.logError(
                "Для обработки передан файл неизвестного формата"
            )
