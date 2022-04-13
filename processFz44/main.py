from contractProjects.ContractProjects import ContractProjects
from _db.DbConnection import DbConnection

if __name__ == "__main__":

    """
        Автор:      Макаров Алексей
        Описание:   Программа по обработке 
                    файлов с информацией о закупках по 44 ФЗ
    """

    a = DbConnection()
    a.makeConnection()
    a.makeConnectionSession()
    a.updateDataBaseModels()

    ContractProjects().processRun()

    a.commitSession()
