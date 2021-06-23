import math

from enum import Enum, auto
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robot.api import logger  # type: ignore
from typing import List, Any

from .argument_utils import is_pabot_testlevelsplit


class Encodings(Enum):
    """
Python comes with a number of codecs built-in,
either implemented as C functions or with dictionaries as mapping tables.
The following table lists the codecs by name,
together with a few common aliases, and the languages for which the encoding is likely used.
Neither the list of aliases nor the list of languages is meant to be exhaustive.
Notice that spelling alternatives that only differ in case or use a hyphen instead
of an underscore are also valid aliases; therefore, e.g. ``utf-8` is a valid alias for the ``utf_8`` codec.

*CPython implementation detail:* Some common encodings can bypass the codecs lookup machinery to improve performance.
These optimization opportunities are only recognized by CPython for a limited set of (case insensitive) aliases:
utf-8, utf8, latin-1, latin1, iso-8859-1, iso8859-1, mbcs (Windows only),
ascii, us-ascii, utf-16, utf16, utf-32, utf32, and the same using underscores instead of dashes.
Using alternative aliases for these encodings may result in slower execution.

Changed in version 3.6: Optimization opportunity recognized for us-ascii.

Many of the character sets support the same languages. They vary in individual characters (e.g. whether the EURO SIGN is supported or not), and in the assignment of characters to code positions. For the European languages in particular, the following variants typically exist:

- utf-8
- cp1252
- an ISO 8859 codeset
- a Microsoft Windows code page, which is typically derived from an 8859 codeset, but replaces control characters with additional graphic characters
- an IBM EBCDIC code page
- an IBM PC code page, which is ASCII compatible
    """
    ascii = auto()
    big5 = auto()
    big5hkscs = auto()
    cp037 = auto()
    cp273 = auto()
    cp424 = auto()
    cp437 = auto()
    cp500 = auto()
    cp720 = auto()
    cp737 = auto()
    cp775 = auto()
    cp850 = auto()
    cp852 = auto()
    cp855 = auto()
    cp856 = auto()
    cp857 = auto()
    cp858 = auto()
    cp860 = auto()
    cp861 = auto()
    cp862 = auto()
    cp863 = auto()
    cp864 = auto()
    cp865 = auto()
    cp866 = auto()
    cp869 = auto()
    cp874 = auto()
    cp875 = auto()
    cp932 = auto()
    cp949 = auto()
    cp950 = auto()
    cp1006 = auto()
    cp1026 = auto()
    cp1125 = auto()
    cp1140 = auto()
    cp1250 = auto()
    cp1251 = auto()
    cp1252 = auto()
    cp1253 = auto()
    cp1254 = auto()
    cp1255 = auto()
    cp1256 = auto()
    cp1257 = auto()
    cp1258 = auto()
    euc_jp = auto()
    euc_jis_2004 = auto()
    euc_jisx0213 = auto()
    euc_kr = auto()
    gb2312 = auto()
    gbk = auto()
    gb18030 = auto()
    hz = auto()
    iso2022_jp = auto()
    iso2022_jp_1 = auto()
    iso2022_jp_2 = auto()
    iso2022_jp_2004 = auto()
    iso2022_jp_3 = auto()
    iso2022_jp_ext = auto()
    iso2022_kr = auto()
    latin_1 = auto()
    iso8859_2 = auto()
    iso8859_3 = auto()
    iso8859_4 = auto()
    iso8859_5 = auto()
    iso8859_6 = auto()
    iso8859_7 = auto()
    iso8859_8 = auto()
    iso8859_9 = auto()
    iso8859_10 = auto()
    iso8859_11 = auto()
    iso8859_13 = auto()
    iso8859_14 = auto()
    iso8859_15 = auto()
    iso8859_16 = auto()
    johab = auto()
    koi8_r = auto()
    koi8_t = auto()
    koi8_u = auto()
    kz1048 = auto()
    mac_cyrillic = auto()
    mac_greek = auto()
    mac_iceland = auto()
    mac_latin2 = auto()
    mac_roman = auto()
    mac_turkish = auto()
    ptcp154 = auto()
    shift_jis = auto()
    shift_jis_2004 = auto()
    shift_jisx0213 = auto()
    utf_32 = auto()
    utf_32_be = auto()
    utf_32_le = auto()
    utf_16 = auto()
    utf_16_be = auto()
    utf_16_le = auto()
    utf_7 = auto()
    utf_8 = auto()
    utf_8_sig = auto()


class PabotOpt(Enum):
    """
You can switch Pabot --testlevelsplit between three modes:

- Equal: means it creates equal sizes groups
- Binary: is more complex. it created a decreasing size of containers to support better balancing.
- Atomic: it does not group tests at all and runs really each test case in a separate thread.

See `Pabot and DataDriver <#pabot-and-datadriver>`__ for more details.

This can be set by ``optimize_pabot`` in Library import.
    """
    Equal = auto()
    Binary = auto()
    Atomic = auto()


def debug(msg: Any, newline: bool = True, stream: str = "stdout"):
    if get_variable_value("${LOG LEVEL}") in ["DEBUG", "TRACE"]:
        logger.console(msg, newline, stream)


def console(msg: Any, newline: bool = True, stream: str = "stdout"):
    logger.console(msg, newline, stream)


def warn(msg: Any, html: bool = False):
    logger.warn(msg, html)


def error(msg: Any, html: bool = False):
    logger.error(msg, html)


def get_filter_dynamic_test_names():
    dynamic_test_list = get_variable_value("${DYNAMICTESTS}")
    if isinstance(dynamic_test_list, str):
        return dynamic_test_list.split("|")
    elif isinstance(dynamic_test_list, list):
        return dynamic_test_list
    else:
        dynamic_test_name = get_variable_value("${DYNAMICTEST}")
        if dynamic_test_name:
            BuiltIn().set_suite_metadata("DataDriver", dynamic_test_name, True)
            return [dynamic_test_name]


def is_pabot_dry_run():
    return is_pabot_testlevelsplit() and get_variable_value("${PABOTQUEUEINDEX}") == "-1"


def get_variable_value(name: str):
    return BuiltIn().get_variable_value(name)


def is_same_keyword(first: str, second: str):
    return _get_normalized_keyword(first) == _get_normalized_keyword(second)


def _get_normalized_keyword(keyword: str):
    return keyword.lower().replace(" ", "").replace("_", "")


def binary_partition_test_list(test_list: List, process_count: int):
    fractions = equally_partition_test_list(test_list, process_count)
    return_list = list()
    for i in range(int(math.sqrt(len(test_list) // process_count))):
        first, second = _partition_second_half(fractions)
        return_list.extend(first)
        fractions = second
    return_list.extend(fractions)
    return [test_name for test_name in return_list if test_name]


def _partition_second_half(fractions):
    first = fractions[: len(fractions) // 2]
    second = list()
    for sub_list in fractions[len(fractions) // 2 :]:
        sub_sub_list = equally_partition_test_list(sub_list, 2)
        second.extend(sub_sub_list)
    return first, second


def equally_partition_test_list(test_list: List, fraction_count: int):
    quotient, remainder = divmod(len(test_list), fraction_count)
    return [
        test_list[i * quotient + min(i, remainder) : (i + 1) * quotient + min(i + 1, remainder)]
        for i in range(fraction_count)
    ]
