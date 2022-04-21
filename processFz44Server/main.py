import sys

from _modules.Logger import Logger

from contractProjects.ContractProjects import ContractProjects


class PrimeProcessClent:

    """
        Автор:          Макаров Алексей
        Описание:       Управление инструментами для обработки данных
    """

    def __init__(self, processToolName: str) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        self.processingTools  = {
            "-contractProjects": ContractProjects
        }
        self.processToolName  = processToolName
        self.dataProcessTool  = self.processingTools.get(self.processToolName)()

        self.sysLoggerManager = Logger()

    def processRunManager(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение запуска инструмента для обработки данных
        """
        
        if self.dataProcessTool is not None:
            self.dataProcessTool.processRun()
        else:
            self.sysLoggerManager.logCritError("При запуске передан неизвестный аргумент")


if __name__ == "__main__":

    """
        Автор:      Макаров Алексей
        Описание:   Программа по обработке 
                    файлов с информацией о закупках по 44 ФЗ
    """

    if len(sys.argv) == 2:
        processTool = PrimeProcessClent(sys.argv[1])
        processTool.processRunManager()
    else:
        Logger().logCritError("При запуске передано неизвестное кол - во аргументов")
