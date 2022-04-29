import datetime

from _modules.servicesServer.ServerViaFTP import ServerViaFTP
from _modules.servicesProgram.ProgramLogger import ProgramLogger


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
        self._currentTimeStamp = datetime.datetime.now()

        self.logger = ProgramLogger()
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
            return f"/fcs_regions/{self.processingRegion}/plangraphs2020/prevMonth/"

        return f"/fcs_regions/{self.processingRegion}/plangraphs2020/currMonth/"

    def __createZakupkiServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения с сервером ftp.zakupki.gov.ru
            Принимаем:
            Возвращаем: 0 - int - Соединение создано
                        1 - int - Соединение не было создано
        """

        if self.zakupkiServerConnection.createConnection() == 1:
            self.logger.logCritError(
                f"Ошибка подключения к серверу для обработки директории {self.__processingZakupkiServerFolderName()}"
            )

        return 0

    def __processingZakupkiServerFolderFile(self, zipFileName: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение обработки файла,
                        содержащего план. графики предстоящих закупок
        """

        self.zakupkiServerConnection.uploadFileInRam(zipFileName)

    def __processingZakupkiServerFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение исследования
                        директории с план. графиками закупок
            Возвращаем: 0 - int - Просмотр
        """

        if self.zakupkiServerConnection.changeProcessPath(
            self.__processingZakupkiServerFolderName()) == 0:

                print(self.zakupkiServerConnection.browseProcessPath())

        return 0

    def processRunForRegion(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса обработки директории
                        региона с файлами, содержащими планы проведения закупок
        """

        self.__createZakupkiServerConnection()
        self.__processingZakupkiServerFolder()

        return 0
