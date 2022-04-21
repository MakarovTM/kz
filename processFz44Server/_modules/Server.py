from _modules.Logger import Logger


class Server:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с удаленным сервером
    """

    def __init__(self, host: str, user: str, pasw: str) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при создании объекта
        """

        self.host = host
        self.user = user
        self.pasw = pasw

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
            Описание:   Удаление подключения с удаленным сервером
        """

        raise NotImplementedError

    def changeProcessPath(self, newProcessPath: str) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Изменение директории на удаленном сервере
        """

        raise NotImplementedError

    def browseProcessPath(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Просмотр директории на удаленном сервере
        """

        raise NotImplemented
