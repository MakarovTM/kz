import unittest

from modules.servicesProgram.ProgramConfig import ProgramConfig


class TestProgramConfig(unittest.TestCase):

    """
        Автор:          Макаров Алексей
        Описание:       Тест для ./modules/servicesProgram/ProgramConfig.py
    """

    def testGetValue(self) -> None:

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение проверки на корректность
                        извлечения данных из конфигурационного файла
        """

        config = ProgramConfig()

        self.assertEqual(
            config.getItem("vm20TradeSu", "host",),
            "vm20.trade.su"
        )


if __name__ == "__main__":
    unittest.main()
