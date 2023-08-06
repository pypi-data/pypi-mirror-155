## Использование

```python
from logsmal import logger

logger.success("Программа запущена", flag="RUN")
```

Создать кастомный логгер. Посмотрите все доступные аргументы
:meth:`logsmal.loglevel.__init__()`

```python
from logsmal import loglevel, logger, CompressionLog

logger.MyLogger = loglevel(
    title_level="[melogger]",
    fileout="./log/mylog.log",
    max_size_file="10kb",
    console_out=False,
    compression=CompressionLog.zip_file
)
```

Работа с уровнями логирования

```python
from logsmal import loglevel, logger

logger.test = loglevel(
    "TEST",
    fileout="./log/log_test.log",
    console_out=False,
    int_level=10
)

loglevel.required_level = 20
logger.test("Текстовое сообщение")
```