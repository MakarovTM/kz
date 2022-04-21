from _db.DbConnection import DbConnection
from contractProjects.ContractProjects import ContractProjects


if __name__ == "__main__":

    """
        Автор:      Макаров Алексей
        Описание:   Программа по обработке 
                    файлов с информацией о закупках по 44 ФЗ
    """

    a = DbConnection()
    a.makeConnection()
    a.makeConnectionSession()

    ContractProjects().processRun()

    a.commitSession()
