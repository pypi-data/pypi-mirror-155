from datetime import datetime
from enum import Enum
from inspect import stack, getframeinfo
from os import path
from typing import Final
from typing import Optional, Any, Callable, Union

from .helpful import MetaLogger
from .independent.helpful import toBitSize
from .independent.log_file import LogFile
from .independent.zip_file import ZippFile, ZipCompression


class CompressionLog(Enum):
    """
    Варианты действий при достижении лимита размера файла
    """
    #: Перезаписать файл (Удалить все и начать с 0)
    rewrite_file = lambda _path_file: CompressionLog._rewrite_file(_path_file)

    #: Сжать лог файл в архив, а после удалить лог файл
    zip_file = lambda _path_file: CompressionLog._zip_file(_path_file)

    @staticmethod
    def _rewrite_file(_path_file: str):
        """Стереть данные из лог файла"""
        _f = LogFile(_path_file)
        logger.system_info(f"{_path_file}:{_f.sizeFile()}", flag="DELETE")
        _f.deleteFile()

    @staticmethod
    def _zip_file(_path_file: str):
        """Сжать лог файл в архив"""
        ZippFile(f"{_path_file}.zip").writeFile(_path_file, compression=ZipCompression.ZIP_LZMA)
        LogFile(_path_file).deleteFile()
        logger.system_info(_path_file, flag="ZIP_AND_DELETE")


class loglevel:
    """
    Создание логгера
    """

    #: Через сколько записей в лог файл, проверять его размер.
    CONT_CHECK_SIZE_LOG_FILE = 10

    # : Значение, которое определяет срабатывания логгера, если у экземпляра логера значение меньше чем это,
    # то он не сработает
    required_level: int = 10

    def __init__(
            self,
            title_logger: str,
            int_level: int = 10,
            fileout: Optional[str] = None,
            console_out: bool = True,
            color_flag: str = "",
            color_title_logger: str = "",
            max_size_file: Optional[Union[int, str]] = "10mb",
            compression: Optional[Union[CompressionLog, Callable]] = None,
            template_file: str = "[{date_now}][{title_logger}][{flag}]:{data}\n",
            template_console: str = "{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}:{data}",
            **kwargs,
    ):
        """
        Создать логгер

        :param title_logger: Название логгера
        :param int_level: Цифровое значение логгера
        :param fileout: Куда записать данные
        :param console_out: Нужно ли выводить данные в ``stdout``
        :param max_size_file: Максимальный размер(байтах), файла после которого происходит ``compression``.

        Также можно указать:

        - kb - Например 10kb
        - mb - Например 1mb
        - None - Без ограничений

        :param compression: Что делать с файлам после достижение ``max_size_file``

        :param template_file: Доступные аргументы в :meth:`allowed_template_loglevel`
        :param template_console: Доступные аргументы в :meth:`allowed_template_loglevel`
        """
        self.title_logger: str = title_logger
        self.fileout: Optional[str] = fileout
        if fileout:
            # Если указан файл, то добавляем функцию для записи в файл
            self._base_logic = lambda data, flag: (self._file_write(data, flag), self._console_print(data, flag))
        else:
            self._base_logic = lambda data, flag: self._console_print(data, flag)

        self.console_out: bool = console_out
        self.color_flag: str = color_flag
        self.color_title_logger: str = color_title_logger
        self.max_size_file: Optional[int] = toBitSize(max_size_file) if max_size_file else None
        self.compression: Callable = compression if compression else CompressionLog.rewrite_file
        self.int_level: int = int_level
        self.template_file: str = template_file
        self.template_console: str = template_console

        #: Сколько раз было записей в лог файл, до выполнения
        #: условия ``self._cont_write_log_file < CONT_CHECK_SIZE_LOG_FILE``
        self._cont_write_log_file = 0

    def __call__(self, data: str, flag: str = ""):
        """
        Вызвать логгер

        :param data:
        :param flag:
        """
        # Если уровень доступа выше или равен требуемому
        if self.int_level >= self.required_level:
            # Выполняем логику логера
            self._base_logic(data, flag)

    def _file_write(self, data: Any, flag: str):
        """
        Метод вызваться для записи в файл

        :param data:
        :param flag:
        """
        # Формируем сообщение в файл
        log_formatted = allowed_template_loglevel(self.template_file, data, flag, self)
        # Записываем в файл
        _f = LogFile(self.fileout)
        _f.appendFile(log_formatted)
        # Проверить размер файла, если размер больше ``self.max_size_file`` то произойдет ``self.compression``
        self._check_size_log_file(_f)

    def _console_print(self, data: Any, flag: str):
        """
        Метод вызваться для вывода данных в консоль

        :param data:
        :param flag:
        """
        # Формируем сообщение в консоль
        log_formatted = allowed_template_loglevel(self.template_console, data, flag, self)
        print(log_formatted)

    def _check_size_log_file(self, _file: LogFile):
        """
        Для оптимизации, проверка размера файла происходит
        при достижении условия определенного количества записи в файл

        :param _file: Файл
        """
        if self._cont_write_log_file > self.CONT_CHECK_SIZE_LOG_FILE or self._cont_write_log_file == 0:
            self._check_compression_log_file(size_file=_file.sizeFile())
        self._cont_write_log_file += 1

    def _check_compression_log_file(self, size_file: int):
        """
        Проверить размер файла.
        Если он превышает ``self.max_size_file`` то  выполнять  ``self.compression``

        :param size_file: Размер файла в байтах
        """
        if self.max_size_file is not None:
            if size_file > self.max_size_file:
                self.compression(self.fileout)

    def _base_logic(self, data: Any, flag: str):
        """
        Логика работы логера

        :param data:
        :param flag:
        """
        ...


class loglevel_extend(loglevel):
    """
    Логгер с расширенной информацией о коде

    В данном случае у нас будет возможность указать место в коде где вызван логгер
    """

    def _file_write(self, data: Any, flag: str):
        # Формируем сообщение в файл
        log_formatted = allowed_template_loglevel.debug_new(self.template_file, data, flag, self)
        # Записываем в файл
        _f = LogFile(self.fileout)
        _f.appendFile(log_formatted)
        # Проверить размер файла, если размер больше ``self.max_size_file`` то произойдет ``self.compression``
        self._check_size_log_file(_f)

    def _console_print(self, data: Any, flag: str):
        # Формируем сообщение в консоль
        log_formatted = allowed_template_loglevel.debug_new(self.template_console, data, flag, self)
        print(log_formatted)


class allowed_template_loglevel:
    """
    Доступные ключи для шаблона лог сообщения в файл

    :Пример передачи:

    ``{level}{flag}{data}\n``
    ``{color_loglevel}{level}{reset}{color_flag}{flag}{reset}``
    """

    def __new__(
            cls,
            _template: str,
            data,
            flag,
            root_loglevel: loglevel
    ) -> str:
        """
        :param _template:
        :param flag:
        :param data:
        """

        return _template.format(
            #  Название логера
            title_logger=root_loglevel.title_logger,
            flag=flag,
            data=data,
            #  Дата создания сообщения
            date_now=datetime.now(),
            # Закрыть цвет
            reset=MetaLogger.reset_,
            #  Цвет заголовка логера
            color_title_logger=root_loglevel.color_title_logger,
            # Цвет флага
            color_flag=root_loglevel.color_flag,
        )

    @classmethod
    def debug_new(
            cls,
            _template: str,
            data,
            flag,
            root_loglevel: loglevel
    ):
        """

        :param root_loglevel:
        :param _template:
        :param flag:
        :param data:
        """

        caller = getframeinfo(stack()[4][0])
        return _template.format(
            #  Название логера
            title_logger=root_loglevel.title_logger,
            flag=flag,
            data=data,
            #  Дата создания сообщения
            date_now=datetime.now(),
            # Закрыть цвет
            reset=MetaLogger.reset_,
            #  Цвет заголовка логера
            color_title_logger=root_loglevel.color_title_logger,
            # Цвет флага
            color_flag=root_loglevel.color_flag,
            # Номер строки
            line_call=caller.lineno,
            # Функция в которой вызвана функция
            func_call=caller.function,
            # Контекст
            context_call=''.join(caller.code_context[0].split()),
            # Абсолютный путь к файлу в котором вызвана функция
            abs_file_call=caller.filename,
            # Файл в котором вызвана функция
            file_call=path.basename(caller.filename)
        )


class logger:
    """
    Стандартные логгеры
    """
    test = loglevel(
        'TEST',
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}:\n{data}",
        color_flag=MetaLogger.gray,
        color_title_logger=MetaLogger.magenta
    )
    debug = loglevel_extend(
        "DEBUG",
        int_level=10,
        color_title_logger=MetaLogger.magenta,
        color_flag=MetaLogger.magenta,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}[{file_call}:{line_call}]:{data}\t\t\t[{context_call}]"
    )
    info = loglevel(
        "INFO",
        int_level=20,
        color_title_logger=MetaLogger.bright_blue,
        color_flag=MetaLogger.yellow,
    )
    success = loglevel(
        "SUCCESS",
        int_level=25,
        color_title_logger=MetaLogger.green,
        color_flag=MetaLogger.gray,
    )
    error = loglevel_extend(
        "ERROR",
        int_level=40,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        template_file="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        color_title_logger=MetaLogger.read,
        color_flag=MetaLogger.yellow,
    )
    warning = loglevel_extend(
        "WARNING",
        int_level=30,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        template_file="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flag}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        color_flag=MetaLogger.read,
        color_title_logger=MetaLogger.yellow,
    )
    #: Логгер для системных задач
    system_info: Final[loglevel] = loglevel(
        "SYSTEM",
        int_level=40,
        color_title_logger=MetaLogger.gray,
        color_flag=MetaLogger.gray,
        console_out=True
    )
    #: Логгер для системных задач
    system_error: Final[loglevel] = loglevel(
        "SYSTEM",
        int_level=45,
        color_title_logger=MetaLogger.gray,
        color_flag=MetaLogger.read,
        console_out=True
    )
