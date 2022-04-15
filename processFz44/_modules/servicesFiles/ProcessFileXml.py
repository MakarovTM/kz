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

        self.dataFormatters = {
            "IsoDateFormatter": self.__formatterIsoDate,
            "FloatP2Formatter": self.__formatterFloatP2,
            "BoolIntFormatter": self.__formatterBoolInt,
        }

        self.__cleanUpNameSpaces()

    def __formatterIsoDate(self, isoDateString: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Форматирование представления времени и даты 
                        от 2022-04-11T14:13:06+07:00 в 2022-04-11 14:13:06 
        """

        return " ".join(isoDateString[:19].split("T"))

    def __formatterFloatP2(self, floatNumString: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Форматирование числа с 
                        точностью до двух знаков после запятой
        """

        return "{:.3f}".format(float(floatNumString))

    def __formatterBoolInt(self, boolArgString: str) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Форматирование булевого выражение в строковом 
                        формате в значение краткого числа, напр. "false" -> 0
        """

        return 0 if boolArgString == "false" else 1

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


    def essenceDataWithXpath(self, essenceStructure: dict, element = None) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных из XML - файла согласно xPath 
        """

        essencedValues = []
        essenceElement = element if element is not None else self.fileContent

        if essenceStructure["multi"] is None:
            essencedValue = essenceElement.find(essenceStructure["xPath"]["parent"])
            if essencedValue is None:
                essencedValues.append(essenceStructure["stand"])
            else:
                essencedValues.append(essencedValue.text)

        if essenceStructure["shape"] is not None:
            essencedValues = [
                self.dataFormatters[essenceStructure["shape"]](essencedValue) 
                for essencedValue in essencedValues
            ]

        return "; ".join(set(list(map(str, essencedValues))))
