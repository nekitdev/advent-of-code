from typing import List

__all__ = ("split_lines", "split_double_lines")

split_lines = str.splitlines

CARRIAGE_RETURN = "\r"
NEW_LINE = "\n"

CARRIAGE_RETURN_NEW_LINE = CARRIAGE_RETURN + NEW_LINE
DOUBLE_NEW_LINE = NEW_LINE + NEW_LINE


def split_double_lines(string: str) -> List[str]:
    return string.replace(CARRIAGE_RETURN_NEW_LINE, NEW_LINE).split(DOUBLE_NEW_LINE)
