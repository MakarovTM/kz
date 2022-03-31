import io
import re
import zipfile


class ZIP_Process:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обработки архивного
    """

    def __init__(self, zip_file_content: io.BytesIO) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке
        """

        self.zip_file_content = zipfile.ZipFile(zip_file_content)

    def zip_file_show_structure(self, filename_mask = None) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Отображение структуры и содержимого архивированного файла,
                        фильтрация содержимого согласно переданной строке regex
        """

        if filename_mask is not None:
            return [i for i in self.zip_file_content.namelist() if re.match(r"{}".format(filename_mask), i)]
        
        return self.zip_file_content.namelist()

    def zip_file_read(self, to_read_filename: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Чтение файла в архиве
        """

        return self.zip_file_content.read(to_read_filename)
