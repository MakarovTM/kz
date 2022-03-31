from modules.services_server.FTP_Server import FTP_Server
from modules.services_files.ZIP_Process import ZIP_Process

from src.notification_prepaid.src.ServerRegionFolderZipFiles import ServerRegionFolderZipFiles


class ServerRegionFolderZip:

	"""
		Автор:			Макаров Алексей
		Описание:		Выполнение обработки архивированного файла на сервере
	"""

	def __init__(self, filename: str, server_connection: FTP_Server) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Инициализация класса 
						по обработке архива с извещениями о осуществлении закупки
		"""

		self.zip_file_in_ram = ZIP_Process(server_connection.upload_server_file_in_ram(filename))

	def run_zip_processing(self) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Выполнение обработки архивированного файла, загруженного в память устройства
		"""

		k = []

		for i in self.zip_file_in_ram.zip_file_show_structure():
			if ".xml" in i:
				m = ServerRegionFolderZipFiles(self.zip_file_in_ram.zip_file_read(i)).essence_purchase_info()
				if m != []:
					k.append(m)

		return k
