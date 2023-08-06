"""
Units
=====
Some common units such as time, number and bytes.
Every unit class is an enum, and has two convert methods, named ``convert_to`` and ``convert_from``.
"""

__all__ = [
    "TimeUnits",
    "NumberUnits",
    "BinaryUnits"
]

from enum import Enum
from typing import Union


_convert_values = {}


class _Converter:
    
    def convert_from(self, number: Union[int, float], src_unit) -> Union[int, float]:
        """
        convert ``number`` from ``src_unit`` to ``self``.

        :param number: a number with int or float type
        :param src_unit: the unit of ``number``
        :return: the return value has the same type with ``number``, it means, if the type of ``number`` is int, the
        method will use integer division.
        """
        return self.__convert(number, src_unit, self)

    def convert_to(self, number: Union[int, float], dst_unit) -> Union[int, float]:
        """
        convert ``number`` from ``self`` to ``dst_unit``.

        :param number: a number with int or float type
        :param dst_unit: the unit of return value
        :return: the return value has the same type with ``number``.
        """
        return self.__convert(number, self, dst_unit)

    @classmethod
    def __convert(cls, number, src_unit, dst_unit):
        if isinstance(src_unit, str):
            src_unit = cls(src_unit)
        if isinstance(dst_unit, str):
            dst_unit = cls(dst_unit)
        if type(src_unit) != type(dst_unit):
            raise TypeError(f"the two units must be equal, but got {type(src_unit)} and {type(dst_unit)}")
        enum_cls = type(src_unit)
        values = _convert_values[enum_cls]
        if isinstance(number, int):
            if values[src_unit] > values[dst_unit]:
                scale = values[src_unit] // values[dst_unit]
                return number * scale
            else:
                scale = values[dst_unit] // values[src_unit]
                return number // scale
        elif isinstance(number, float):
            if values[src_unit] > values[dst_unit]:
                scale = values[src_unit] // values[dst_unit]
                return number * scale
            else:
                scale = values[dst_unit] // values[src_unit]
                return number / scale
        else:
            raise TypeError(f"the type of number must be int or float, not {type(number)}")


class TimeUnits(_Converter, Enum):
    """
    Time Units
    ==========
    The time units, from nanoseconds up to hours.
    """
    NANO = "ns"
    MICRO = "us"
    MILLI = "ms"
    SECOND = "s"
    MINUTE = "m"
    HOUR = "h"


_time_values = {
    TimeUnits.NANO: 1,
    TimeUnits.MICRO: 1000,
    TimeUnits.MILLI: 1000000,
    TimeUnits.SECOND: 1000000000,
    TimeUnits.MINUTE: 60000000000,
    TimeUnits.HOUR: 3600000000000
}
_convert_values[TimeUnits] = _time_values


class NumberUnits(_Converter, Enum):
    """
    Number Units
    ============
    The decimal number unit, from one up to peta(1e15).
    """
    BASE = "b"
    DECA = "d"
    HECTO = "h"
    KILO = "k"
    MEGA = "m"
    GIGA = "g"
    TERA = "t"
    PETA = "p"
    
    
_number_values = {
    NumberUnits.BASE: 1,
    NumberUnits.DECA: 10,
    NumberUnits.HECTO: 100,
    NumberUnits.KILO: 1000,
    NumberUnits.MEGA: 1000000,
    NumberUnits.GIGA: 1000000000,
    NumberUnits.TERA: 1000000000000,
    NumberUnits.PETA: 1000000000000000
}
_convert_values[NumberUnits] = _number_values


class BinaryUnits(_Converter, Enum):
    """
    Binary Units
    ============
    The bit units and byte units, from B(b) up to PiB(b).
    """
    
    b = "b"
    B = "B"
    Kib = "Kib"
    KiB = "KiB"
    Mib = "Mib"
    MiB = "MiB"
    Gib = "Gib"
    GiB = "GiB"
    Tib = "Tib"
    TiB = "TiB"
    Pib = "Pib"
    PiB = "PiB"
    

_binary_values = {
    BinaryUnits.b: 1,
    BinaryUnits.B: 8,
    BinaryUnits.Kib: 1024,
    BinaryUnits.KiB: 8192,
    BinaryUnits.Mib: 1048576,
    BinaryUnits.MiB: 8388608,
    BinaryUnits.Gib: 1073741824,
    BinaryUnits.GiB: 8589934592,
    BinaryUnits.Tib: 1099511627776,
    BinaryUnits.TiB: 8796093022208,
    BinaryUnits.Pib: 1125899906842624,
    BinaryUnits.PiB: 9007199254740992
}
_convert_values[BinaryUnits] = _binary_values
