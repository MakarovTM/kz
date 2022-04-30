from _modules.servicesProgram.ProgramLogger import ProgramLogger


class Server:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с удаленным сервером
    """

    def __init__(self, host: str, user: str, pasw: str, port: int) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при создании объекта
        """

        self._host = host
        self._port = port
        self._user = user
        self._pasw = pasw
        self._serverConnection = None

        self._logger = ProgramLogger()

    def createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание подключения с удаленным сервером
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

        raise NotImplementedError
