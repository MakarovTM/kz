from sshtunnel import SSHTunnelForwarder

from _modules.Server import Server


class ServerViaSsh(Server):

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для работы
                        с удаленным сервером через SSH соединение
    """

    def createConnection(self) -> int:
        
        """
            Автор:      Макаров Алексей
            Описание:   Выполнение подключения к серверу
        """

        try:
            self.serverConnection = SSHTunnelForwarder(
                (self.host, int(self.port)), 
                ssh_username = self.user, ssh_password = self.pasw,
                remote_bind_address = (self.dbHost, int(self.dbPort))
            )
            self.serverConnection.start()
        except Exception as e:
            self.sysLoggerManager.logCritError(
                f"Ошибка при подключении к серверу - {self.host}  - {str(e)}"
            )
        
        return 0

    def deleteConnection(self) -> int:
        
        """
            Автор:      Макаров Алексей
            Описание:   Разрываем подключение
                        с удаленным сервером через протокол SSH
        """

        try:
            self.serverConnection.stop()
        except Exception as e:
            print(e)

        return 0
