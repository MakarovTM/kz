import ftplib

from _modules.Server import Server


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

    def browseProcessPath(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение просмотра
                        активной директории на удаленном сервере
        """

        if self.serverConnection is not None:
            return self.serverConnection.nlst()
        else:
            self.sysLoggerManager.logCritError(
                "Просмотр активной директории невозможен, тк не было создано подключение"
            )

        return []
