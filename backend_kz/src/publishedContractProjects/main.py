from src.publishedContractProjects.src.ServerRegionFolder import ServerRegionFolder
from db.DB_Connection import DB_Connection

from vars.fz44ProcessRegions import fz44ProcessRegions

from tqdm import tqdm

def main():

    """
        Автор:      Макаров Алексей
        Описание:   Точка входа в инструмент 
                    по созданию хронологии заключения контракта поставщиком
    """

    dbConnection = DB_Connection()
    if dbConnection.makeConnection() == 0:
        if dbConnection.makeConnectionSession() == 0:
            print("Подключение к базе данных создано")

    for fz44ProcessRegion in tqdm(fz44ProcessRegions):
        ServerRegionFolder(fz44ProcessRegion).runServerRegionFolderProcessing()

    dbConnection.commitSession()
