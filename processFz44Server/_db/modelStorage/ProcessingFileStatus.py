import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import SmallInteger

from _db.DbModelsStorage import Base


class ProcessingFileStatus(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, хранящая информацию
                    о статусе обработке файлов на FTP сервере
    """

    __tablename__ = "fz44ProcessingFileStatus"

    id = Column(Integer, primary_key=True)
    filename = Column(String(length=100), unique=True)
    status = Column(SmallInteger(), default=0)
    ts = Column(DateTime(), default=datetime.datetime.utcnow)
