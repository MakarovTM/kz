from _modules.Logger import Logger
from _vars.processingRegions import fz44ProcessingRegions

from planGraphs.src.PlanGraphsProcessRegion import PlanGraphsProcessRegion


class PlanGraphs:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обработки директории, содержащей 
                    информацию о заплонированных процедурах проведения торгов
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        self.logger = Logger()

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение процесса обработки файлов с 
                        информацией об опубликованных торгах в директории региона
        """

        for i in fz44ProcessingRegions:
            if PlanGraphsProcessRegion(i).processRunForRegion() == 0:
                self.logger.logInfo(f"Processing {i} region folder finished")
            else:
                self.logger.logCritError(f"Processing {i} region folder not finished")

        return 0
