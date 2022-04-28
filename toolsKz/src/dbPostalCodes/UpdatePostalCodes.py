import pickle
from dbfread import DBF


class UpdatePostalCodes:

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение парсинга данных о почтовых индексах РФ
        Источник:       https://www.pochta.ru/support/database/ops    
    """

    def __init__(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self._dbConnection = None
        self._dbServerConnection = None

        self.pathPostalCodeDb = "/Users/makarov/Downloads/PIndx07.dbf"

    def __retrievalData(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение извлечения данных
            Возвращаем: 0 - Извлечение данных выполнено успешно
        """

        self.postalCodesData = {
            record["INDEX"]: {
                "placeCityName":   record["CITY"] if record["CITY"] != "" else record["REGION"],
                "placeRegionName": record["REGION"],
            }
            for record in DBF(self.pathPostalCodeDb)
        }

        return 0

    def __saveDataToPyDbFile(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение сохранения данных в БД
        """

        with open("basePostalCodes.pkl", "wb") as dbFile:
            pickle.dump(self.postalCodesData, dbFile)

        return 0

    def processRun(self) -> int:

        """
            Автор:      Макаров Алексей
            Описание:   Запуск процесса парсинга сведение о почтовых индексах РФ
        """

        if self.__retrievalData() == 0:
            if self.__saveDataToPyDbFile() == 0:
                print("Данные о регионах РФ и почтовых кодах обновлены")

        return 0
