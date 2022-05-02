from tqdm import tqdm
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

        processingInternalFolder = "prevMonth" \
            if datetime.now().strftime("%d") == "1" else "currMonth"

        return [
            "/fcs_regions/{}/{}/{}/".format(
                processingRegionFolder,
                self._processingFolder, processingInternalFolder
            ) for processingRegionFolder in self._fz44ProcessingRegions
        ]

    def runProcessingFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки данных
        """

        for processingServerPath in tqdm(self.__processingRegionFolderNames()):
            ProcessingFolderRegion(processingServerPath)
            break
