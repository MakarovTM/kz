from modules.services_files.XML_Process import XML_Process


class ServerRegionFolderZipFiles:

	"""
		Автор:			Макаров Алексей
		Описание:		Выполнение обработки архивированного файла, 
						содержащего информацию о закупке на FTP сервере
	"""

	def __init__(self, mmm) -> None:

		"""
			Автор:		Макаров Алексей
			Описание:	Инициализация класса по обработке файла
		"""

		self.xml_file_object = XML_Process(mmm)
		self.xml_essence_tags = [
			["commonInfo", "purchaseNumber"],
			["commonInfo", "purchaseObjectInfo"],
			["responsibleOrgInfo", "INN"],
			["responsibleOrgInfo", "fullName"],
			["maxPriceInfo", "maxPrice"],
			["OKPD2", "OKPDCode"],
			["advancePaymentSum", "sumInPercents"],
			["contractGuarantee", "amount"],
			["collectingInfo", "startDT"],
			["collectingInfo", "endDT"]
		]

	def __essence_purchase_param(self, tag_parent, tag_child) -> str:

		"""
			Автор:		Макаров Алексей
			Описание:	Выполнение поиска информации об
		"""

		return self.xml_file_object.get_value_by_tag_name(tag_parent, tag_child)

	def essence_purchase_info(self) -> list:

		"""
			Автор:		Макаров Алексей
			Описание:	Извлечение информации из файла по заданным тэгам
		"""
		_ = []
		for i in self.xml_essence_tags:
			_.append(self.__essence_purchase_param(i[0], i[1]))
			
		return _ if _[6] != "" else []
