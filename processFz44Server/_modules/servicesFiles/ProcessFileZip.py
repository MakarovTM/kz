from re import match
from io import BytesIO
from zipfile import ZipFile

from _modules.servicesProgram.Logger import Logger


class ProcessFileZip:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе с файлами, им. расш. *.zip
    """

    def __init__(self, zipFileContent: BytesIO) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Инициализация класса по обработке
            Получаем  : {
                            varType: BytesIO,
                            varName: zipFileContent,
                            varDesc: Буфер байтов в памяти, содержимое файла
                        }
        """

        self._logger = Logger()
        self._zipFileContent = ZipFile(zipFileContent)

    def showStructureOfZip(self, fileNameMask: str) -> list:

        """
            Автор     : Макаров Алексей
            Описание  : Отображение содержимого, фильтрация
                        содержимого согласно шаблону регулярного выражения
            Получаем  : {
                            varType: Str,
                            varName: fileNameMask,
                            varDesc: Шаблон регулярного выражения
                        }
            Возвращем : {
                            varType: List,
                            varName: containedFileNames,
                            varDesc: Список файлов внутри архива,
                                     наименование которых удоволетв. шаблону
                        }
        """

        containedFileNames = self._zipFileContent.namelist()

        if fileNameMask is not None:
            return [
                i for i in containedFileNames if match(f"{fileNameMask}", i)
            ]

        return containedFileNames

    def readZipFileContent(self, fileName: str) -> str:

        """
            Автор     : Макаров Алексей
            Описание  : Выполнение чтения файла внутри архива
            Получаем  : {
                            varType: Str,
                            varName: fileName,
                            varDesc: Наименование файла
                                     для чтения в оперативную память
                        }
            Возвращем : {
                            varType: Bytes,
                            varDesc: Содержимое файла, в формате неизменяемой
                                     последовательности отдельных байтов
                        }
        """

        try:
            return self._zipFileContent.read(fileName)
        except Exception as e:
            self._logger.logCritError(
                f"Ошибка при попытке чтения файла в архиве - {str(e)}"
            )

        return ""
