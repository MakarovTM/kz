from sshtunnel import SSHTunnelForwarder

from modules.servicesProgram.ProgramConfig import ProgramConfig


class ServerVm20ViaSSH(ProgramConfig):

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с сервером
                        vm20.trade.su посредством SSH соединения
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации класса
        """

        ProgramConfig.__init__(self)

        self._host = self.getItem("vm20TradeSu", "host")
        self._port = int(self.getItem("vm20TradeSu", "port"))

        self._user = self.getItem("vm20TradeSu", "user")
        self._pasw = self.getItem("vm20TradeSu", "pasw")

        self._dbHost = self.getItem("vm20TradeSu", "dbHost")
        self._dbPort = int(self.getItem("vm20TradeSu", "dbPort"))

        self._serverConnection = None

        if self.__createConnection() == 0:
            print("Соединнение с сервером vm20.trade.su успешно установлено")

    def __del__(self):

        if self._serverConnection is not None:
            self.__deleteConnection()
            print("Отработал деструктор")

    def __createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение соединения с сервером
        """

        try:
            self._serverConnection = SSHTunnelForwarder(
                ssh_address_or_host=(self._host, self._port),
                ssh_username=self._user, ssh_password=self._pasw,
                remote_bind_address=(self._dbHost, self._dbPort)
            )
            self._serverConnection.start()
        except Exception as e:
            print(e)
            return 1

        return 0

    def __deleteConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение удаления соединения с сервером
        """

        if self._serverConnection is not None:
            self._serverConnection.close
            return 1

        return 0

    def showLocalBindPort(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Получение номера порта для соединения с БД
        """

        if self._serverConnection is None:
            return 1

        return self._serverConnection.local_bind_port
