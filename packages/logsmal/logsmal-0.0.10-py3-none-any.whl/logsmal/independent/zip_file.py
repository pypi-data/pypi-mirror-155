from enum import Enum
from os import path, listdir
from typing import Optional, Any, Callable
from zipfile import ZIP_LZMA, ZipFile, ZIP_DEFLATED, ZIP_BZIP2, ZIP_STORED

from .log_file import BaseFile


class ZipCompression(Enum):
    """
    Степень сжатия, чем ниже тем больше
    """
    ZIP_STORED = ZIP_STORED
    ZIP_DEFLATED = ZIP_DEFLATED
    ZIP_BZIP2 = ZIP_BZIP2
    ZIP_LZMA = ZIP_LZMA


class ZippFile(BaseFile):
    """
    Работа с архивом
    """

    def __init__(
            self, name_file: str, type_file: Optional[str] = ".zip",
            call_log_info: Callable[[str, str], None] = lambda _x, flag: ...,
            call_log_error: Callable[[str, str], None] = lambda _x, flag: ...,
    ):
        super().__init__(name_file, type_file=type_file)
        self.call_log_info: Callable[[str, str], None] = call_log_info
        self.call_log_error: Callable[[str, str], None] = call_log_error

    def writeFile(self, in_path: str, compression: ZipCompression = ZipCompression.ZIP_DEFLATED, arcname=None):
        """
        Записать файл в архив

        :param in_path: Путь к файлу
        :param compression: Степень сжатия файла
        :param arcname: По какому пути будет расположен файл в архиве
        """
        with ZipFile(self.name_file, 'w', compression=compression.value) as zip_file:
            if path.isfile(in_path):
                zip_file.write(in_path, arcname)


    def writePath(self,
                  in_path: str,
                  execute_path: Optional[set[str]] = None,
                  compression: ZipCompression = ZipCompression.ZIP_DEFLATED
                  ):

        """
        Заархивировать файлы и папки из указанного пути

        :param in_path: Путь к папке в которой нужно все за архивировать.
          Кроме того что указано в аргументе ``execute_path``
        :param execute_path: Что не архивировать
        :param compression: Сжатие файла
        """
        # Если исключений нет, то множеств пустое
        if execute_path is None:
            execute_path = set()
        # Если файл, то архивируем его, если папка, то рекурсивно
        # архивируем каждый файл
        with ZipFile(self.name_file, 'w', compression=compression.value) as zip_file:
            if path.isfile(in_path):
                zip_file.write(in_path)
            else:
                self._addFolderToZip(
                    zip_file,
                    in_path,
                    _base_folder=in_path,
                    execute_path=execute_path
                )

    def _addFolderToZip(
            self,
            zip_file: ZipFile,
            in_folder: str,
            execute_path: set[str],
            _base_folder: str
    ):
        """
        Рекурсивная архивация директории

        :param zip_file: Дескриптор архива
        :param in_folder: Текущая директория
        :param execute_path: Что не нужно архивировать
        :param _base_folder: Главный путь в котором происходит архивация
            именно его мы отсечем от абсолютно пути, и запишем относительный путь в архив
        """
        #: Имя текущего архива
        name_self_zip_file: str = path.basename(zip_file.filename)
        for file in listdir(in_folder):
            # Мы не должны архивировать свой же архив, и те что в исключении
            if file != name_self_zip_file and file not in execute_path:
                full_path = path.join(in_folder, file)
                if path.isfile(full_path):
                    zip_file.write(
                        full_path,
                        # Нам не нужен полный путь в архиве, поэтому мы его заменим на относительный
                        arcname=full_path.replace(_base_folder, '')
                    )
                    self.call_log_info(full_path, flag="FILE_ADD")
                elif path.isdir(full_path):
                    self._addFolderToZip(
                        zip_file,
                        full_path,
                        execute_path,
                        _base_folder
                    )
                    self.call_log_info(full_path, flag="FOLDER_ADD")

            else:
                self.call_log_info(file, flag="SKIP")

    def readFile(self, *arg) -> Any:
        pass

    def appendFile(self, arg: Any):
        pass
