from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from _db.DbModelsStorage import Base


class PurchaseProtocolFinal(Base):

    """
        Автор:      Макаров Алексей
        Описание:   Модель данных, хранящая информацию
                    о финале проведения процедуры закупок
    """

    __tablename__ = "purchaseProtocolFinal"

    id = Column(Integer, primary_key=True)
    purchaseNum = Column(String(length=50), unique=True)
    purchaseReasonAbandoned = Column(String(length=50))
