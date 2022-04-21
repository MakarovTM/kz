from lxml import etree


class ProcessFileXml:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по обработке файла с .xml расширением
    """

    def __init__(self, binarXmlContent: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self.fileContent = etree.fromstring(binarXmlContent)
