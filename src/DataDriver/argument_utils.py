import sys

from enum import IntEnum

from robot.run import USAGE
from robot.utils.argumentparser import ArgumentParser

SINGLE_ARG_CHARACTERS = '.?hTX'


class ArgumentState(IntEnum):
    ANALYZE_NEXT = 0
    ONE_KNOWN = 1
    TWO_KNOWN = 2


def robot_options():
    arg_parser = ArgumentParser(USAGE, auto_pythonpath=False, auto_argumentfile=True, env_options='ROBOT_OPTIONS')
    valid_args = _filter_args(arg_parser)
    return arg_parser.parse_args(valid_args)[0]


def _filter_args(arg_parser):
    short_opts = arg_parser._short_opts
    long_opts = arg_parser._long_opts
    arg_state = 0
    valid_robot_args = list()
    for arg in sys.argv[1:]:
        if arg_state == ArgumentState.ANALYZE_NEXT:
            arg_state = _get_argument_state(arg, short_opts, long_opts)
        if arg_state >= ArgumentState.ONE_KNOWN:
            valid_robot_args.append(arg)
            arg_state -= 1
    return valid_robot_args


def _get_argument_state(arg, short_opts, long_opts):
    param_opt = [l_opt[:-1] for l_opt in long_opts if l_opt[-1:] == '=']
    arg_state = 0
    if _is_short_option(arg):
        if arg[1] in SINGLE_ARG_CHARACTERS:
            arg_state = ArgumentState.ONE_KNOWN
        elif arg[1] in short_opts:
            arg_state = ArgumentState.TWO_KNOWN
    elif _is_long_option(arg):
        if arg[2:] in param_opt:
            arg_state = ArgumentState.TWO_KNOWN
        elif arg[2:] in long_opts:
            arg_state = ArgumentState.ONE_KNOWN
    return arg_state


def _is_short_option(arg):
    return len(arg) == 2 and arg[0] == '-'


def _is_long_option(arg):
    return len(arg) > 2 and arg[:2] == '--'
