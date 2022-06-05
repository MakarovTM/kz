from sqlalchemy import Column
from sqlalchemy import Integer

from db.DbModelsStorage import Base


class Test(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Тестовая таблица для проверки
                    работоспособности и проведения UNIT - тестирования
    """

    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    id1 = Column(Integer)
