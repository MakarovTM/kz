from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from sqlalchemy.orm import validates

from _db.DbModelsStorage import Base


class UnscheduledChecks(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, хранящая информацию
                    о незапланированных процедурах проверок
    """

    __tablename__ = "fz44UnscheduledChecks"

    id = Column(Integer, primary_key=True)
    regNumber = Column(String(length=25), unique=True)
    ispectorInn = Column(String(length=25))
    ispectorName = Column(String(length=500))
    inspectedInn = Column(String(length=25))
    inspectedName = Column(String(length=500))
    noticeDescription = Column(Text())
    inspectionPlannedDate = Column(Date())
    inspectionPublishedDate = Column(Date())
    printFormUrl = Column(String(length=100))

    @validates("inspectionPlannedDate", "inspectionPublishedDate")
    def validateColumnValue(self, columnName, columnValue):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение форматирования данных при записи в БД
        """

        if columnName in (
            "inspectionPlannedDate",
            "inspectionPublishedDate"
        ):
            return columnValue[:10]
