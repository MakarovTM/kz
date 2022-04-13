import requests

from tqdm import tqdm
PROXIES_PATH = "/Users/makarov/Documents/kz/temp/oldProxies.txt"


def read_proxies_ips():

    """
        Автор:      Макаров Алексей
        Описание:   Чтение файла с ip адерсами прокси серверов
    """

    with open(PROXIES_PATH, "r") as file:
        lines = [line.rstrip() for line in file]

    return lines


def check_proxies_url(proxies_urls: list):

    """
        Автор:      Макаров Алексей
        Описание:   Проверка прокси адресов
    """

    clear_proxies_url = []

    for proxies_url in tqdm(proxies_urls):
        try:
            proxy_dict = {
                "https": proxies_url
            }
            _ = requests.get("https://zakupki.gov.ru/epz/main/public/home.html", proxies = proxy_dict, timeout = 3)
            if _.status_code == 200:
                clear_proxies_url.append(proxies_url)
        except:
            print("error")

    with open('clear_proxies.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(clear_proxies_url))


if __name__ == "__main__":

    proxies_urls = read_proxies_ips()
    print(proxies_urls)

    check_proxies_url(proxies_urls)
