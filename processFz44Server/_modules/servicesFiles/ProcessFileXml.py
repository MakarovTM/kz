from lxml import etree


class ProcessFileXml:

    """
        Автор:      Макаров Алексей
        Описание:   Модуль по работе с файлами, им. расш. *.xml
    """

    def __init__(self, xmlFileContent: bytes) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Магический метод, выполняемый при инициализации объекта
            Получаем  : {
                            varType: bytes,
                            varName: xmlFileContent,
                            varDesc: Буфер байтов в памяти aka содержимое файла
                        }
        """

        self._fileContent = etree.fromstring(xmlFileContent)

    def __cleanUpNameSpaces(self) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Удаление пространства имён из .xml файла
        """

        for elem in self._fileContent.getiterator():
            if not isinstance(elem, (etree._Comment, etree._ProcessingInstruction)):
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(self._fileContent)
