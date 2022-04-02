import io
import re

from db.DB_Connection import DB_Connection
from db.DB_Models     import ContractProjectTimeLine

from modules.services_files.ZIP_Process import ZIP_Process


class ServerRegionFolderZip:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки архивированных файлов, 
                        содержащих информацию о процедуре заключения контракта
    """


    def __init__(self, zipedCpFiles: io.BytesIO) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса 
                        по обработке файла с прокетами контрактов
        """

        self.dbConnection = DB_Connection()
        self.zipedCpFiles = ZIP_Process(zipedCpFiles)

    def __createContractProjectMileStone(self, purchaseNumber: str):

        """
            Автор:      Макаров Алексей
            Описание:   Создание записи о опубликованном проекте контракта
        """

        if self.dbConnection.dbConSession.query(ContractProjectTimeLine).\
            filter(ContractProjectTimeLine.pnb == purchaseNumber) is not None:
                self.dbConnection.dbConSession.add(
                    ContractProjectTimeLine(pnb = purchaseNumber, hpb = 1)
                )

    def __updateContractProjectMileStone(self, purchaseNumber: str, column: str):

        """
            Автор:      Макаров Алексей
            Описание:   Обновление записи о хронологии процесса заключения контракта
        """

        self.dbConnection.dbConSession.query(ContractProjectTimeLine).\
            filter(ContractProjectTimeLine.pnb == purchaseNumber).\
                update({column : 1})

    def updateContractProjectsTimeLine(self):

        """
            Автор:      Макаров Алексей
            Описание:   Обновление хронологии процедуры заключения контракта
        """

        for i in self.zipedCpFiles.zipFileShowStructure(filename_mask = r".*.xml"):

            purchaseNumber = re.findall(r"_(\d+)_", i)[0]

