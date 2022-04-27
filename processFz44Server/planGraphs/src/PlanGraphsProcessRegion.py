import datetime

from _modules.Logger import Logger
from _modules.ServerViaFTP import ServerViaFTP


class PlanGraphsProcessRegion:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки
                        директории региона с планами проведения процедуры закупок
    """

    def __init__(self, processRegion: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        self.processingRegion = processRegion

        self.logger = Logger()
        self.zakupkiServerConnection = ServerViaFTP("ftp.zakupki.gov.ru", "free", "free")

    def __processingZakupkiServerFolderName(self) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Генерирование имени директории
                        для обработке файлов, содержащихся в ней
            Принимаем:
            Возвращаем: str - Полный путь к обрабатываемой директории
        """

        if datetime.datetime.now().strftime("%d") == "1":
            return f"/fcs_regions/{self.processRegion}/contractprojects/prevMonth/"

        return f"/fcs_regions/{self.processRegion}/contractprojects/currMonth/"

    def __makeZakupkiServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения с сервером ftp.zakupki.gov.ru
            Принимаем:
            Возвращаем: 0 - int - Соединение создано
                        1 - int - Соединение не было создано
        """

        if self.zakupkiServerConnection.createConnection() == 1:
            self.logger.logCritError(
                f"Creating connection to process folder {self.__processingZakupkiServerFolderName()} failed"
            )

        return 0

    def processRunForRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории 
                        региона с файлами, содержащими планы проведения закупок
        """

        self.__makeZakupkiServerConnection()

        return 0
