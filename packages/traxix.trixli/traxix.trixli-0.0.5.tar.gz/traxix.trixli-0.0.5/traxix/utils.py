import os
import re


def colorize(line, regexps):
    RED = "\033[31"
    BACK = "\033[m"
    for regexp in regexps:
        line = re.sub(regexp, Color.RED + r"\1" + Color.ENDC, line)

    return line


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    RED = "\033[31m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _match(string, regexps, regexps_neg=None):
    for regexp in regexps:
        if re.search(regexp, string) is None:
            return False
        if (
            regexps_neg is not None
            and re.search(regexps_neg, string) is not None
        ):
            return False
    return True


def _matches(string, regexps):
    matches = []
    for regexp in regexps:
        result = re.search(regexp, string)
        if result is None:
            return False
        matches.append(result)

    return result


def _compile_re(regexps, with_group: bool = True):
    if with_group:
        return [re.compile("(" + str(regexp) + ")") for regexp in regexps]
    else:
        return [re.compile(str(regexp)) for regexp in regexps]


def _f(*args, p="."):
    compiled_re = _compile_re(regexps=args)
    for root, dirs, files in os.walk(p, topdown=False):
        for name in files:
            full_path = os.path.join(root, name)
            if _match(string=full_path, regexps=compiled_re):
                yield full_path
