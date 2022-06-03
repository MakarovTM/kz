from fuzzywuzzy import fuzz

from sqlalchemy import event

from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import validates

from _db.DbModelsStorage import Base


class PurchaseNotifications(Base):

    """
        Автор:          Макаров Алексей
        Описание:       Модель данных, описывающая размещенные уведомлении
                        об осуществлении проведения процедуры закупки
    """

    __tablename__ = "fz44PurchaseNotifications"

    id = Column(Integer, primary_key=True)
    purchaseNum = Column(String(length=50), unique=True)
    purchaseObj = Column(String(length=1000))
    purchasePrc = Column(Float(10, 2))
    placingFrom = Column(Date())
    placingTill = Column(Date())
    customerInn = Column(String(length=30))
    purchaseIkz = Column(String(length=50))
    referenceTo = Column(Integer, ForeignKey("fz44PurchaseNotifications.id"))
    publishedEIS = Column(Date())
    similarScore = Column(Integer)

    @validates("placingFrom", "placingTill", "publishedEIS")
    def validateColumnValue(self, columnName, columnValue):

        """
            Автор:      Макаров Алексей
            Описание:   Выполнение форматирования данных при записи в БД
        """

        if columnName in ("placingTill", "placingFrom", "publishedEIS"):
            return columnValue[:10]


@event.listens_for(PurchaseNotifications, "before_insert")
def setCustomerInn(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение извлечения
                        ИНН заказчика перед сохранением данных
    """

    target.customerInn = target.purchaseIkz[3:13]


@event.listens_for(PurchaseNotifications, "before_insert")
def setReferencedPurchase(mapper, connection, target):

    """
        Автор:          Макаров Алексей
        Описание:       Выполнение поиска похожей закупки
    """

    fetchResults = connection.execute(
        """
            SELECT
                `id`, `purchaseNum`, `purchaseObj`
            FROM
                `purchaseNotifications`
            WHERE
                `customerInn` = '{}' AND `purchasePrc` >= {}
        """.format(target.purchaseIkz[3:13], target.purchasePrc)
    )

    similarPurchases = [
        fetchedRow
        for fetchedRow in fetchResults if fetchedRow[1] != target.purchaseNum
    ]

    if not similarPurchases:
        target.referenceTo = None
    else:
        similarScores = {
            fuzz.token_sort_ratio(
                target.purchaseObj, similarPurchase[2]): similarPurchase[0]
            for similarPurchase in similarPurchases
        }
        maxSimilarScore = max(list(similarScores.keys()))
        if maxSimilarScore >= 85:
            target.referenceTo = similarScores[maxSimilarScore]
            target.similarScore = maxSimilarScore
        else:
            target.referenceTo = None
            target.similarScore = None
