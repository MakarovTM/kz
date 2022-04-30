import datetime

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
from _modules.servicesProgram.ProgramLogger import ProgramLogger


class ContractProjectsProcessRegion:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки
                        директории региона с проектами контрактов
    """

    def __init__(self, processRegion: str) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self.sysLoggerManager = Logger()
        self.serverConnection = ServerViaFTP("ftp.zakupki.gov.ru", "free", "free")

        self.toProcessRegion  = processRegion
        self.currentTimeStamp = datetime.datetime.now()

    def __del__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при деинициализации объекта
        """

        self.__deleteServerConnection()

    def __processingFolderName(self) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Получение наименования директории для последующей
        """

        if self.currentTimeStamp.strftime("%d") == "1":
            return f"/fcs_regions/{self.toProcessRegion}/contractprojects/prevMonth/"

        return f"/fcs_regions/{self.toProcessRegion}/contractprojects/currMonth/"

    def __createServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение подключения к удаленному серверу
        """

        if self.serverConnection.createConnection() == 0:
            self.sysLoggerManager.logInfo(
                f"Для обработки директории ({self.__processingFolderName()}) создано подключение к серверу"
            )
        else:
            self.sysLoggerManager.logError(
                f"Для обработки директории ({self.__processingFolderName()}) не было создано подключение к серверу"
            )
            return 1

        return 0

    def __deleteServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение 
        """

        if self.serverConnection.deleteConnection() == 0:
            self.sysLoggerManager.logInfo(
                f"Closed server connection : ({self.__processingFolderName()})"
            )
        else:
            self.sysLoggerManager.logError(
                f"Closing server connection error : ({self.__processingFolderName()})"
            )

    def __changeServerWorkFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Смена активной директории на сервере
        """

        if self.serverConnection.changeProcessPath(self.__processingFolderName()) == 0:

            self.sysLoggerManager.logInfo(
                f"Changed server work folder to - {self.__processingFolderName()}"
            )
        
        else:

            self.sysLoggerManager.logCritError(
                f"Failed to change server work folder to - {self.__processingFolderName()}" 
            )


    def __toProcessFileNamesList(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Получение списка файлов для выполнения и обработки
        """

    def processRegionRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение процесса 
                        обработки директории с проектами контрактов
        """

        self.__createServerConnection()

        # self.serverConnection.changeProcessPath(self.__processingFolderName())
        # print(self.serverConnection.browseProcessPath())


        return 0
