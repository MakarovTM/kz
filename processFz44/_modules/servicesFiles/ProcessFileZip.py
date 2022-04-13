import io
import re
import zipfile


class ProcessFileZip:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обработки архивного
    """

    def __init__(self, zip_file_content: io.BytesIO) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке
        """

        self.zipFileContent = zipfile.ZipFile(zip_file_content)

    def zipFileShowStructure(self, fileNameMask = None) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Отображение структуры и содержимого архивированного файла,
                        фильтрация содержимого согласно переданной строке regex
        """

        if fileNameMask is not None:
            return [i for i in self.zipFileContent.namelist() if re.match(r"{}".format(fileNameMask), i)]
        
        return self.zipFileContent.namelist()

    def readFilesIntoArchive(self, toReadFileName: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Чтение файла в архиве
        """

        return self.zipFileContent.read(toReadFileName)
