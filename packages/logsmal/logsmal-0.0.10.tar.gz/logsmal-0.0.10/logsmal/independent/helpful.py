import re
from typing import Union


def toBitSize(size: Union[str, int]) -> int:
    """
    :param size:
    можно указать:
        - kb - Например 10kb
        - mb - Например 1mb

    >>> toBitSize("10kb")
    10240
    >>> toBitSize("1mb")
    1048576
    >>> toBitSize("1gb")
    Traceback (most recent call last):
    ValueError: Не верный тип 1gb
    """
    match size:
        case int():
            return size
        case str() as _res if _r := re.match("([\d_]+)kb|KB", _res):
            return int(_r.group(1)) * 1024
        case str() as _res if _r := re.match("([\d_]+)mb|MB", _res):
            return int(_r.group(1)) * 1048576
        case _:
            raise ValueError(f"Не верный тип {size}")
