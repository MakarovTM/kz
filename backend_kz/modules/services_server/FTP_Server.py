import io
import re
import ftplib


class FTP_Server:

	"""
		Автор:			Макаров Алексей
		Описание:		Выполнение работы с 
						удаленным сервером посредством FTP - соединения
	"""

	def __init__(self, host: str, user: str, password: str) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Инициализация класса по работе с удаленным сервером
		"""

		self.server_connection = ftplib.FTP(host = host, user = user, passwd = password)

	def __del__(self) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Деструктор класса по работе с удаленным сервером
		"""

		self.server_connection.quit()

	def change_server_folder(self, to_change_server_folder: str) -> int:

		"""
			Автор:		Макаров Алексей
			Описание:	Смена активной директории на удаленном сервере
		"""

		try:
			self.server_connection.cwd(to_change_server_folder)
		except Exception as e:
			return 1

		return 0

	def listing_server_folder(self, filter_string = None) -> list:

		"""
			Автор:		Макаров Алексей
			Описание:	Отображение содержимого в текущей директории на удаленном сервере
		"""

		if filter_string is None:
			return self.server_connection.nlst()
		else:
			return [i for i in self.server_connection.nlst() if filter_string in i]

	def upload_server_file_in_ram(self, to_upload_filename: str) -> str:

		"""
			Автор:		Макаров Алексей
			Описание:	Выполнение загрузки файла с сервера в опреативную память устройства
		"""

		ram_file_buffer = io.BytesIO()
		self.server_connection.retrbinary(f"RETR {to_upload_filename}", ram_file_buffer.write)

		return ram_file_buffer
