from lxml import etree

from _modules.servicesProgram.ProgramLogger import ProgramLogger


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
            if not isinstance(
                    elem, (etree._Comment, etree._ProcessingInstruction)):
                elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(self._fileContent)

        return 0

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

        essencedValues = []

        if not essenceStructure["multi"]:
            essencedElem = self.\
                _fileContent.find(essenceStructure["xPath"]["parent"])
            if essencedElem is not None:
                essencedValues.append(essencedElem.text)
            else:
                essencedValues.append(essenceStructure["default"])

        return "; ".join(set(list(map(str, essencedValues))))
