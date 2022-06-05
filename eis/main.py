from db.DbConnection import DbConnection


if __name__ == "__main__":

    """
        Автор:      Макаров Алексей
        Описание:   Точка входа в программу, обеспечивающей
                    обработку информации, размещаемой внутри ЕИС
    """

    a = DbConnection()
    a.updateDbModelStorage()
