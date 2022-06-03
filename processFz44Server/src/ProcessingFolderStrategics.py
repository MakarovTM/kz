import re

from io import BytesIO

from src.protocols.ProtocolsFinal import ProtocolsFinal
from src.unplannedCheck.UnplannedCheck import UnplannedCheck
from src.notifications.EpNotificationsEF2020 import EpNotificationsEF2020

from _modules.servicesProgram.ProgramLogger import ProgramLogger


class ProcessingFolderStrategics:

    """
        Автор:          Макаров Алексей
        Описание:       Поведенческий паттерн, управляющий
                        процессом извлечения данных из XML файлов с закупками
    """

    def __init__(
        self,
        fileName: str, fileContent: BytesIO, dbConnection
    ) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self.filename = fileName

        self._essenceDataTool = None

        self._logger = ProgramLogger()
        self._dbConnection = dbConnection

        if re.match(r"unplannedCheck_.*.xml", fileName):
            self._essenceDataTool = UnplannedCheck(fileContent, self._dbConnection)

        if re.match(r"epNotificationE.*.xml", fileName):
            self._essenceDataTool = EpNotificationsEF2020(fileContent)

        if re.match(r"epProtocol.*Final.*.xml", fileName):
            print("here1")
            self._essenceDataTool = ProtocolsFinal(fileContent)

    def checkProcessingStrategics(self) -> bool:

        """
            Автор:      Макаров Алексей
            Описание:   Проверка на выбор стратегии обработки файла
        """

        return True if self._essenceDataTool is not None else False

    def showEssencedData(self) -> None:

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
