import io

from tqdm import tqdm

from modules.services_files.ZIP_Process import ZIP_Process

from src.notification_republished.src.purchasePlanGraths.ServerRegionFolderZipFile import ServerRegionFolderZipFile


class ServerRegionFolderZip:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки архивированных файлов, 
                        содержащих информацию об осущенствлении закупки
    """

    def __init__(self, ziped_purchases: io.BytesIO) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке архивированного файла 
        """

        self.ziped_purchases = ZIP_Process(ziped_purchases)
        self.ziped_purchases_filename_mask = r"tenderPlan2020[_\d]+.xml"
    
    def run_archived_purchases_processing(self):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение запуска процесса обработки архивированного файла
        """

        for purchase_file in tqdm(self.ziped_purchases.zipFileShowStructure(self.ziped_purchases_filename_mask)):
            ServerRegionFolderZipFile(
                self.ziped_purchases.zip_file_read(purchase_file)
            ).essenceData()
