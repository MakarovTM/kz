from db.DB_Connection import DB_Connection
# from src.notification_republished.src.purchasePlanGraths.ServerRegionFolder import ServerRegionFolderPG
from src.notification_republished.src.purchaseProtocols.ServerRegionFolder import ServerRegionFolder

def main():

    """
        Автор:      Макаров Алексей
        Описание:   Точка входа в программу по поиску извещений, 
                    повторно размещенных в ЕИС из-за отсутсвия участников
    """

    dbConnection = DB_Connection()
    if dbConnection.makeConnection() == 0:
        if dbConnection.makeConnectionSession() == 0:
            print("Подключение к базе данных создано")

    # ServerRegionFolderPG("Moskva").run_region_folder_processing()
    ServerRegionFolder("Moskva").run_region_folder_processing()

