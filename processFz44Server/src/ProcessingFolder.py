from datetime import datetime

from src.ProcessingFolderRegion import ProcessingFolderRegion

from _vars.fz44ProcessingRegions import fz44ProcessingRegions


class ProcessingFolder:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение подготовки директории к обработке данных
    """

    def __init__(self, processingFolder: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        self._processingFolder = processingFolder
        self._fz44ProcessingRegions = fz44ProcessingRegions

    def __processingRegionFolderNames(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Генерирование имени директории
                        для обработки файлов, содержащихся в ней
        """

        if self._processingFolder == "fcs_fas":
            return [
                "/fcs_fas/unplannedCheck/{}".format(
                    "prevMonth" if datetime.now().strftime("%d") == "1" else "currMonth"
                )
            ]

    def runProcessingFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки данных
        """

        for processingServerPath in self.__processingRegionFolderNames():
            ProcessingFolderRegion(
                processingServerPath
            ).runProcessFolderRegion()
