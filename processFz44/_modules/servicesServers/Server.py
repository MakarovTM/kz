class Server:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение работ с удаленным серверами
    """

    def __init__(self, host: str, user: str, pasw: str) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по работе с удаленным сервером
        """

        self.host = host
        self.user = user
        self.pasw = pasw

        self.serverConnection = None

    def createConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Создание соединения с сервером
        """

        raise NotImplemented

    def deleteConnection(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Уничтожение соединения с сервером
        """

        raise NotImplemented

    def changeWorkFolder(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Изменение активной директории на сервере
        """

        raise NotImplemented

    def viewOpenedFolder(self) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Отображение содержимого текущей директории
        """

        raise NotImplemented

    def uploadFolderFile(self, toBeUploadedFile: str):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение загрузки файлов в оперативную память устройства
        """

        raise NotImplemented
