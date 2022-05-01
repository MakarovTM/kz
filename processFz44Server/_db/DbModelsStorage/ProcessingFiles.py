from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import SmallInteger

from _db.DbModelsStorage import Base


class ZakupkiServerFilesProcessingStatus(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, описывающая статус процедуры
                    обработки файлов, размещенных на FTP сервере
    """

    __tablename__ = "zakupkiServerFilesProcessingStatus"

    id = Column(String(length=10), primary_key=True)
    name = Column(String(length=200), unique=True)
    status = Column(SmallInteger(length=1), default=0)
