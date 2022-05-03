import sys
from io import BytesIO
from lxml import etree
from sqlalchemy import except_all

from _modules.servicesProgram.ProgramLogger import ProgramLogger


class ProcessFileXml:

    """
        Автор:      Макаров Алексей
        Описание:   Модуль по работе с файлами, им. расш. *.xml
    """

    def __init__(self, xmlFileContent: BytesIO) -> None:

        """
            Автор     : Макаров Алексей
            Описание  : Магический метод, выполняемый при инициализации объекта
            Получаем  : {
                            varType:    bytes,
                            varName:    xmlFileContent,
                            varDesc:    Буфер байтов в памяти
                        }
        """

        self._logger = ProgramLogger()

        try:
            self._fileContent = etree.fromstring(xmlFileContent)
            if self.__cleanUpNameSpaces() != 0:
                self._logger.logError(
                    "Произошла ошибка при удалении пространства имен"
                )
        except Exception:
            self._logger.logError(
                "При инициализации класса был передан некорректный файл"
            )

    def __cleanUpNameSpaces(self) -> int:

        """
            Автор     : Макаров Алексей
            Описание  : Удаление пространства имён из .xml файла
        """

        for elem in self._fileContent.getiterator():
            elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(self._fileContent)

        return 0

    def __createNewRootIterator(self, newRootIterator: str):

        """
            Автор:      Макаров Алексей
            Описание:   Создание итератора дерева XML
                        файла с переданным элементов в качестве корня
        """

        return [
            newRoot
            for newRoot in self._fileContent.find(newRootIterator)
        ]

    def essenceDataWithXpath(self, essenceStructure: dict) -> str:

        """
            Автор     : Макаров Алексей
            Описание  : Выполнение извлечения
                        данных из XML файла согласно переданной структуре
            Получаем  : {
                            varType:    Dict,
                            varName:    essenceStructure,
                            varDesc:    Структура,
                                        описывающая извлекаемые данные
                            varTree:    {

                                            varType:    Bool,
                                            varName:    multi,
                                            varDesc:    Искомое значение
                                                        содержится в потомках

                                            varType:    Dict,
                                            varName:    xPath
                                            varDesc:    Словарь со знач. xPath
                                                        для извлечения данных
                                                        из узлов документа

                                            varType:    Dict Elem,
                                            varName:    parent,
                                            varDesc:    Значение единое:
                                                            xPath узла
                                                        Значение множеств:
                                                            xPath корн. узла

                                            varType:    Dict Elem,
                                            varName:    nested,
                                            varDesc:    Значение множеств:
                                                            xPath узла

                                            varType:    Str,
                                            varName:    default,
                                            varDesc:    Значение для
                                                        узла по умолчанию

                                        }
                        }
            Возвращаем: {
                            varType:    Str,
                            varDesc:    Полученное значение по заданному ключу
                        }
        """

        def essenceDataFromRoot(essenceDataRoot) -> dict:

            """
                Автор:          Макаров Алексей
                Описание:       Выполнение извлечения
                                данных из корневого элемента
            """

            def essenceDataValue(essenceNewSubRoot, essenceSubSwitch):

                essencedValue = essenceNewSubRoot.find(essenceSubSwitch)

                return None if essencedValue is None else essencedValue.text

            for essenceSwitch in list(essenceStructure.keys())[1:]:
                if essenceStructure[essenceSwitch]["multi"]:
                    _ = essenceDataRoot.find(essenceStructure[essenceSwitch]["xPath"]["parent"])
                    if _ is not None:
                        a = []
                        for newSubRoot in _:
                            if newSubRoot.tag == essenceStructure[essenceSwitch]["xPath"]["nested"]:
                                a.append(newSubRoot.text)
                        print(a)
                    else:
                        print("ОКВЭД не указаны")
                else:
                    print(essenceDataValue(essenceDataRoot, essenceStructure[essenceSwitch]["xPath"]["parent"]))

        try:
            rootElements = self.__createNewRootIterator(
                essenceStructure["config"]["stackedRoot"]
            ) if essenceStructure["config"]["stacked"] else [self._fileContent]

            for i in rootElements:
                try:
                    essenceDataFromRoot(i)
                except Exception as e:
                    print(etree.tostring(self._fileContent).decode())
                    print(e)
                    sys.exit(0)
        except:
           
           pass
            
