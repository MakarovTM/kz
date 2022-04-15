import logging


class Logger:

    """
        Автор:          Макаров Алексей
        Описание:       Модуль, выполняющий логгирование процесса выполнения кода
    """

    def __new__(cls) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при создании объекта
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(Logger, cls).__new__(cls)
            cls.instance.cСonstructed = False

        return cls.instance

    def __init__(self) -> None:
        
        """
            Автор:      Макаров Алексей
            Описание:   Магический метод, выполняемый при инициализации объекта
        """

        if not self.cСonstructed:

            self.cСonstructed = True

