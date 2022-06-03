from sshtunnel import SSHTunnelForwarder

from _modules.servicesProgram.ProgramLogger import ProgramLogger
from _modules.servicesProgram.ProgramConfig import ProgramConfig


class ServerViaSsh():

    """
        Автор:          Макаров Алексей
        Описание:       Модуль для работы
                        с удаленным сервером через SSH соединение
    """

    def __init__(
        self,
        host: str, port: int, user: str, pasw: str,
        dbHost=None, dbPort=None
    ) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        if self.cСonstructed:

            self._host = host
            self._port = port
            self._user = user
            self._pasw = pasw

            self._dbHost = dbHost
            self._dbPort = dbPort

            self._serverConnection = None

            self._logger = ProgramLogger()
            self._config = ProgramConfig()

    def __new__(cls, *args, **kwargs):

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при создании объекта
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(ServerViaSsh, cls).__new__(cls)
            cls.instance.cСonstructed = True

        return cls.instance

    def createServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения
                        с сервером посредством SSH соединения
        """

        try:
            self._serverConnection = SSHTunnelForwarder(
                (
                    self._host, int(self._port),
                ),
                ssh_username=self._user,
                ssh_password=self._pasw,
                remote_bind_address=(
                    self._dbHost, int(self._dbPort),
                )
            )
            self._serverConnection.start()
        except Exception as e:
            self._logger.logError(
                f"Ошибка при создании объекта SSH подключения - {str(e)}"
            )
            return 1

        return 0

    def deleteServerConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение разрушения соединения с сервером
        """

        self._serverConnection.close()

        return 0

    def showLocalBindPort(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Отображения порта подключения к серверу
        """

        return self._serverConnection.local_bind_port
