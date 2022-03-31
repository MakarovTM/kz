from src.notification_prepaid.src.ServerRegionFolder import ServerRegionFolder
import pandas as pd

def main():

    """
        Автор:      Макаров Алексей
        Описание:   Точка входа в программу
                    по поиску извещений, отвечающих следующим требованиям:
                    1) ЦФО
                    2) Авансирование заявки
    """

    r = []
    r = r + ServerRegionFolder("Moskva").make_server_connection()
    print(r)

    r = pd.DataFrame(r)
    r.to_excel("prepaid_notifications.xlsx")