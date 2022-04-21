from _modules.Logger import Logger


class Server:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с удаленным сервером
    """

    def __init__(
        self, host: str, port: int, user: str, pasw: str, dbHost = None, dbPort = None) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при создании объекта
        """

        self.host = host
        self.port = port
        self.user = user
        self.pasw = pasw

        self.dbHost = dbHost
        self.dbPort = dbPort

        self.serverConnection = None
        self.sysLoggerManager = Logger()

    def createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения с удаленным сервером
        """
    
        raise NotImplementedError

    def deleteConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Разрываем подключение с удаленным сервером
        """

        raise NotImplementedError
