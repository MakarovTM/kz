import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer, Float

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RepublishedNotifications(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, содержащая
                    информацию о переопубликованных контрактах 
    """

    __tablename__ = "republished_notifications"

    id  = Column(Integer, primary_key = True)
    ikz = Column(String(length = 50), unique = True)
    obj = Column(String(length = 500))
    prc = Column(Float())
    crn = Column(String(length = 50))
    okv = Column(String(length = 500))
    rid = Column(Integer, ForeignKey("republished_notifications.id"))
    pnb = Column(String(length = 20))
    pdt = Column(DateTime)
    cdt = Column(DateTime, default = datetime.datetime.utcnow)
    udt = Column(DateTime)


def main(db_connection) -> int:

    """
        Автор:      Макаров Алексей
        Описание:   Создание моделей в базе данных
    """

    Base.metadata.create_all(db_connection)

    return 0
