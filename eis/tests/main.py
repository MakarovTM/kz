from operator import mod
import unittest

from tests.testsCases.TestProgramConfig import TestProgramConfig


def runTests():

    """
        Автор:      Макаров Алексей
        Описание:   Выполнение запуска процедуры тестирования написанного кода
    """

    suite = unittest.TestLoader().loadTestsFromModule(
        TestProgramConfig
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
