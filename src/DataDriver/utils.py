import math

from enum import Enum, auto
from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robot.api import logger  # type: ignore
from typing import List, Any

from .argument_utils import is_pabot_testlevelsplit


class PabotOpt(Enum):
    Equal = auto()
    Binary = auto()
    Atomic = auto()


def debug(msg: Any, newline: bool = True, stream: str = "stdout"):
    if get_variable_value("${LOG LEVEL}") in ["DEBUG", "TRACE"]:
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
