import io
import ftplib

from _modules.servicesServers.Server import Server


class ServerViaFTP(Server):

    """
        Автор:          Макаров Алексей
        Описание:       Взаимодействие с удаленным сервером через FTP соединение
    """

    def createConnection(self) -> int:

        try:
            self.serverConnection = ftplib.FTP(
                host = self.host, user = self.user, passwd = self.pasw, timeout = 3)
            self.serverConnection.set_pasv(False)
        except Exception as e:
            print(e)
        
        return 0

    def deleteConnection(self) -> int:

        if not self.serverConnection:
           self.serverConnection.quit()
        else:
            return 1
        
        return 0

    def viewOpenedFolder(self) -> list:
        
        return self.serverConnection.nlst() if self.serverConnection is not None else []

    def inloadFolderFile(self, toBeInloadedFile: str):

        ramFileBuffer = io.BytesIO()
        self.serverConnection.retrbinary(f"RETR {toBeInloadedFile}", ramFileBuffer.write)

        return ramFileBuffer

    def changeWorkFolder(self, toChangeFolderPath: str) -> int:

        if self.serverConnection is not None:
            self.serverConnection.cwd(toChangeFolderPath)

        return 0