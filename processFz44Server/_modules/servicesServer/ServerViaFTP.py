from re import match
from io import BytesIO
from ftplib import FTP

from _modules.servicesServer.Server import Server


class ServerViaFTP(Server):

    """
        Автор:          Макаров Алексей
        Описание:       Модуль по работе
                        с удаленным сервером через протокол FTP
    """

    def createConnection(self) -> int:

        """
            Автор     : Макаров Алексей
            Описание  : Создание подключения
                        с удаленным сервером через протокол FTP
            Возвращем : {
                            varType: Int,
                            varDesc: 0 - Соединение было успешно создано
                        }
        """

        try:
            self._serverConnection = FTP(
                host=self._host, port=self._port, user=self._user,
                passwd=self._pasw, timeout=10
            )
        except Exception as e:
            self._logger.logError(
                f"Ошибка создания соед. с сервером {self._host} - {str(e)}"
            )

        return 0

    def changeProcessPath(self, newProcessPath: str) -> int:

        """
            Автор     : Макаров Алексей
            Описание  : Выполнение смены
                        активной директории на удаленном сервере
            Принимаем : {
                            varType: Str,
                            varName: newProcessPath,
                            varDesc: Абсолютный путь для смены
                                     текущего рабочего каталога на сервере
                        }
            Возвращем : {
                            varType: Int,
                            varDesc: 0 - Соединение было успешно создано
                        }
        """

        if self._serverConnection is None:
            self._logger.logError(
                "Смена рабочего каталога невозможна из-за отсутвия подключения"
            )
        else:
            try:
                self._serverConnection.cwd(newProcessPath)
            except Exception:
                self._logger.logError(
                    "Для смены рабочего каталога был передан неизвестный путь"
                )

        return 0

    def browseProcessPath(self, fileNameMask: str) -> list:

        """
            Автор     : Макаров Алексей
            Описание  : Выполнение просмотра
                        содержимого рабочего каталога на сервере
            Принимаем : {
                            varType: Str,
                            varName: filterString,
                            varDesc: Шаблон регулярного выражения
                        }
            Возвращем : {
                            varType: List,
                            varDesc: Список файлов в рабочем каталоге,
                                     наименование которых удоволетв. шаблону
                        }
        """

        if self._serverConnection is None:
            self._logger.logError(
                "Просмотр директории невозможен, тк соединения не существует")
        else:

            containedFileNames = self._serverConnection.nlst()

            if fileNameMask is not None:
                return [
                    i
                    for i in containedFileNames if match(f"{fileNameMask}", i)
                ]

            return containedFileNames

        return []

    def uploadFileInRam(self, toUploadFileName: str) -> BytesIO:

        """
            Автор     :     Макаров Алексей
            Описание  :     Выполнение загрузки файла,
                            расположенного на FTP сервере в память устройства
            Принимаем : {
                            varType: str,
                            varName: toUploadFileName,
                            varDesc: Наименование файла для загрузки
                        }
            Возвращаем: {
                            varType: BytesIO,
                            varName: ramFileBuffer,
                            varDesc: Буфер байтов в памяти, содержимое файла
                        }
        """

        ramFileBuffer = BytesIO()

        if self.serverConnection is None:
            self.sysLoggerManager.logCritError(
                "Отсутсвует активное соединение с сервером для загрузки файла"
            )
        else:
            self.serverConnection.retrbinary(
                f"RETR {toUploadFileName}", ramFileBuffer.write)

        return ramFileBuffer
