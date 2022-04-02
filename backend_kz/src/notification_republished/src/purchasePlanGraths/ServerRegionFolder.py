import datetime
from tqdm import tqdm
from modules.services_server.FTP_Server import FTP_Server

from src.notification_republished.src.purchasePlanGraths.ServerRegionFolderZip import ServerRegionFolderZip


class ServerRegionFolder:

	"""
		Автор:			Макаров Алексей
		Описание:		Выполнение обработки директории,
						содержащей архивы с информацией о предстоящей закупке
	"""

	def __init__(self, processing_region: str) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Инициализация класса по обработке директории на сервере
		"""

		self.processing_region = processing_region
		self.current_timestamp = datetime.datetime.now()
		self.current_timestamp = datetime.datetime(2022, 3, 31, 18, 00)
		self.server_connection = FTP_Server("ftp.zakupki.gov.ru", "free", "free")

	def __to_process_server_path(self) -> str:

		"""
			Автор:      Макаров Алексей
			Описание:   Определяем путь к директории, 
						для которой выполняется обработка файлов
		"""

		if self.current_timestamp.strftime("%d") == "1":
			return f"/fcs_regions/{self.processing_region}/plangraphs2020/prevMonth/"

		return f"/fcs_regions/{self.processing_region}/plangraphs2020/"

	def __to_process_server_files(self, mode = None) -> list:

		"""
			Автор:		Макаров Алексей
			Описание:	Получение списка файлов на сервере для последующей обработки
		"""

		# self.current_timestamp.strftime("%Y%m%d")

		if mode is not None:
			return self.server_connection.listing_server_folder(
				filter_string = "2021"
			)[2:3]
		
		return self.server_connection.listing_server_folder()


	def run_region_folder_processing(self) -> int:

		"""
			Автор:		Макаров Алексей
			Описание:	Запуск процесса 
						обработки директории с извещениями о проведении закупки
		"""

		if self.server_connection.change_server_folder(self.__to_process_server_path()) == 0:
			for archived in tqdm(self.__to_process_server_files(mode = 1)):
				print(archived)
				ServerRegionFolderZip(
					self.server_connection.upload_server_file_in_ram(archived)
				).run_archived_purchases_processing()
