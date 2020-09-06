from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from .argument_utils import is_pabot_testlevelsplit


def debug(msg, newline=True, stream="stdout"):
    if get_variable_value("${LOG LEVEL}") in ["DEBUG", "TRACE"]:
        logger.console(msg, newline, stream)


def warn(msg, html=False):
    logger.warn(msg, html)


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


def get_variable_value(name):
    return BuiltIn().get_variable_value(name)


def is_same_keyword(first, second):
    return _get_normalized_keyword(first) == _get_normalized_keyword(second)


def _get_normalized_keyword(keyword):
    return keyword.lower().replace(" ", "").replace("_", "")
