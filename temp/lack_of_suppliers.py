import os
import re
import pandas as pd
import xml.etree.ElementTree as ET

from tqdm import tqdm

# Путь, в котором лежат загруженные папки
FOLDERS_PATH = "/Users/makarov/Desktop/zakupki_ftp_storage"


# Чтение папок, содержащих файлы с протоколами проведения закупки
folders = [i for i in os.listdir(path = FOLDERS_PATH) if not i.startswith(".")]


# Создание системных путей к файлам с протоколами проведения закупки
to_protocols_paths = []
for folder in folders:
	file_path = f"{FOLDERS_PATH}/{folder}"
	to_protocols_paths = to_protocols_paths + [f"{file_path}/{i}" for i in os.listdir(file_path) if ".xml" in i and not re.search(r"fcsProtocol.*615", i)]


# Поиск атрибута в протоколе, показывающего, что не было подано ни одной заявки
abandoned_protocols = []
for to_protocol_path in tqdm(to_protocols_paths):
	root = ET.parse(to_protocol_path).getroot()
	for elem in root.iter():
		if "abandonedReason" in elem.tag:
			for i in elem:
				if "code" in i.tag:
					abandoned_protocols.append(
						[
							re.findall(r"\d{19}", to_protocol_path)[0], i.text[-2:]
						]
					)

# Выгрузка информации в CSV файл
abandoned_protocols_df = pd.DataFrame(abandoned_protocols)
abandoned_protocols_df.to_csv("abandoned_protocols.csv", index = False, header = False)
