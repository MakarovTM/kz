import xml.etree.ElementTree as ET


class XML_Process:

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение обработки файла в формате XML
    """

    def __init__(self, xml_file_content: bytes) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Инициализация класса по обработке XML файла
        """

        self.fileContent = ET.fromstring(xml_file_content)

    def createNewRootIterator(self, newRootTag: str):

        """
            Автор:      Макаров Алексей
            Описание:   Создание итератора дерева XML 
                        файла с переданным элементов в качестве корня
        """

        newRoots = []

        for newRoot in self.fileContent.iter(newRootTag):
            if len(newRoot) != 0: newRoots.append(newRoot)

        return newRoots

    def essenceDataWithNeighbours(
        self, tagParent: str, tagChild: str, element = None) -> str:

        """
            Автор:      Макаров Алексей
            Описание:   Извлечение значения из XML дерева 
                        согласно значению родительских и дочерних тегов элемента
        """

        essencedValues = []
        essenceElement = element if element is not None else self.fileContent

        for essenceTagParent in essenceElement.iter():
            if tagParent in essenceTagParent.tag:
                for essenceTagChild in essenceTagParent:
                    if tagChild in essenceTagChild.tag:
                        essencedValues.append(essenceTagChild.text)

        return "; ".join(set(essencedValues))
