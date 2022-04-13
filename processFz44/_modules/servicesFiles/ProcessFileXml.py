import datetime
from lxml import etree


def isoDateFormatter(isoDateString: str) -> str:

    """
        Автор:      Макаров Алексей
        Описание:   Изменение формата даты и времени
    """

    return " ".join(isoDateString[:19].split("T"))


class ProcessFileXml:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение обработки файла в формате XML
    """

    def __init__(self, xml_file_content: bytes) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке XML файла
        """

        self.fileContent = etree.fromstring(xml_file_content)

        self.formatters = {
            "IsoDateFormatter": isoDateFormatter
        }

        self.__cleanUpNameSpaces()

    def __cleanUpNameSpaces(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Удаление пространства имен из XML файла
        """

        for elem in self.fileContent.getiterator():
            if not isinstance(elem, (etree._Comment, etree._ProcessingInstruction)):
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(self.fileContent)

    def createNewRootIterator(self, newRootTag: str) -> list:

        """
            Автор:      Макаров Алексей
            Описание:   Создание итератора дерева XML 
                        файла с переданным элементов в качестве корня
        """

        newRoots = []

        for newRoot in self.fileContent.getiterator(newRootTag):
            if len(newRoot) != 0: 
                newRoots.append(newRoot)

        return newRoots

    def showSTR(self):

        print(etree.tostring(self.fileContent).decode())

    def __createRootIterator(self, rootTag: str, rootElement = None) -> tuple:

        """
            Автор:      Макаров Алексей
            Описание:   Создание нового корневого элемента
        """

        rootElement = rootElement if rootElement is not None else self.fileContent

        return (childRoot for childRoot in rootElement.getiterator(rootTag) if len(childRoot) != 0)

    def essenceDataWithPaths(self, essencePaths: list, multi = False, element = None, shape = None) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Извлечение данных из XML дерева согласно URI 
        """

        essencedValues = []
        essenceElement = element if element is not None else self.fileContent

        if multi == True:
            for elem in self.__createRootIterator(essencePaths[0], element):
                essencedValues.append(elem.find(essencePaths[1]).text)
        else:
            if essenceElement.find(essencePaths[0]) is not None:
                essencedValues.append(essenceElement.find(essencePaths[0]).text)

        if shape is not None:
            return " ".join(set([self.formatters[shape](i) for i in essencedValues]))

        return "; ".join(set(essencedValues))
