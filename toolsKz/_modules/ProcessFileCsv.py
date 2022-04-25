import pandas as pd


class ProcessFileCsv:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по обработке файла с .csv расширением
    """

    def __init__(self, csvFileContent: bytes) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод,
                        выполняемый при инициализации объекта
        """

        self.pdDataFrame = pd.read_csv(csvFileContent)