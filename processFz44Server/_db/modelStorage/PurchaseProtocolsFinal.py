from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from sqlalchemy.orm import validates

from _db.DbModelsStorage import Base


class PurchaseProtocolsFinal(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, хранящая информацию
                    о финале проведения процедуры закупок
    """

    __tablename__ = "fz44PurchaseProtocolsFinal"

    id = Column(Integer, primary_key=True)
    purchaseNum = Column(String(length=50), unique=True)
    purchaseReasonAbandoned = Column(String(length=50))

    @validates("purchaseReasonAbandoned")
    def validateColumnValue(self, columnName, columnValue):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение форматирования данных при записи в БД
        """

        if columnName in ("purchaseReasonAbandoned"):
            return columnValue[-2:] if columnValue != "" else ""
