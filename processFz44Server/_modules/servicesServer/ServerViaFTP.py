from io import BytesIO
import ftplib

from _modules.servicesServer.Server import Server


class ServerViaFTP(Server):

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе
                        с удаленным сервером через протокол FTP
    """

    def createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения
                        с удаленным сервером через протокол FTP
        """

        try:
            self.serverConnection = ftplib.FTP(
                host = self.host, user = self.user, passwd = self.pasw, timeout = 10
            )
        except Exception as e:
            self.sysLoggerManager.logCritError(
                f"Произошла ошибка при создании подключения с FTP сервером - {str(e)}"
            )
            return 1

        return 0

    def deleteConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Разрыв подключения
                        с удаленным сервером через протокол FTP
        """

        if self.serverConnection is not None:
            try:
                self.serverConnection.quit()
            except Exception as e:
                self.sysLoggerManager.logError(
                    f"Произошла ошибка при разрыве подключения с сервером - {str(e)}"
                )
                return 1
        else:
            self.sysLoggerManager.logCritError(
                "Соединение не было создано для его посл. разрыва"
            )
            return 2

        return 0

    def changeProcessPath(self, newProcessPath: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение смены
                        активной директории на удаленном сервере
        """

        if self.serverConnection is not None:
            try:
                self.serverConnection.cwd(newProcessPath)
            except Exception as e:
                self.sysLoggerManager.logError(
                    f"Произошла ошибка при смене директории на сервере - {str(e)}"
                )
                return 1
        else:
            self.sysLoggerManager.logCritError(
                "Смена активной директории невозможна, тк не было создано подключение"
            )
            return 2

        return 0

    def browseProcessPath(self, filterString: str) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение просмотра
                        активной директории на удаленном сервере
        """

        if self.serverConnection is not None:
            if filterString is None:
                return self.serverConnection.nlst()
            else:
                return [i for i in self.serverConnection.nlst() if i in filterString]
        else:
            self.sysLoggerManager.logCritError(
                "Просмотр активной директории невозможен, тк не было создано подключение"
            )

        return []

    def uploadFileInRam(self, toUploadFileName: str) -> BytesIO:

        """
            Автор     :     Макаров Алексей
            Описание  :     Выполнение загрузки файла,
                            расположенного на FTP сервере в память устройства
            Принимаем : {
                            varType: str,
                            varName: toUploadFileName,
                            varDesc: Наименование файла для загрузки
                        }
            Возвращаем: {
                            varType: BytesIO,
                            varName: ramFileBuffer,
                            varDesc: Буфер байтов в памяти, содержимое файла
                        }
        """

        ramFileBuffer = BytesIO()

        if self.serverConnection is None:
            self.sysLoggerManager.logCritError(
                "Отсутсвует активное соединение с сервером для загрузки файла"
            )
        else:
            self.serverConnection.retrbinary(
                f"RETR {toUploadFileName}", ramFileBuffer.write)

        return ramFileBuffer
