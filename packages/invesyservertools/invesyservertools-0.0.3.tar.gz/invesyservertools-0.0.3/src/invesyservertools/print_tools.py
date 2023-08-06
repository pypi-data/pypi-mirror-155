# -*- coding: utf-8 -*-
import os
import re
import textwrap
from colorama import Fore, Style

LIST_BULLET = '-'
COLOR_RESET = getattr(Style, 'RESET_ALL')

INDENT_MULT = 4
INDENT_BASE = 4 * ' '

UNIT_PREFIXES = {
    'binary': ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'],
    'decimal': ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
}


## human-readable list
#
# creates a human-readable list, including "and"
# (or any similar word, i.e. in another language)
def and_list(
    elements: list,
    et: str = 'and'
) -> str:
    elements = [str(el) for el in elements]
    return re.sub(
        r', (\w+)$', r' {} \1'.format(et),
        ', '.join(elements)
    )


def indent(
    level: int = 1,
    raw: bool = False,
    base: int = INDENT_MULT,
    base_str: str = ' '
) -> int:
    base = base * base_str
    if raw:
        return base * level
    else:
        return (base * level)[:-1]


##  Enhanced print function
#
#   The arguments (strings) can contain '\n',
#   either as a singleton or as part of a string argument
#
#   @param texts: all the texts as a list
#   @param logging: you have to provide the logging object
#   @param indent: set the indentation level
#   @param list_bullet: True or provide a string
#   @param color: can be a string or a dictionary: {index: color}.
#                 Example: {1: 'red', 4: 'blue'}.
#                 index begins with 1
#                 strings containing only line endings ('\n') don't count!
#   @param style
#   @param sep: as in print function
#   @param end: as in print function
#   @param ignore: don't print (but possibly log)
#   @param flush: as in print function
#   @param nowrapper: don't use textwrap
def print_(
    *texts: list,
    logging: bool = False,
    indent: int = 0,
    list_bullet: (bool, str) = '',
    color: (str, dict) = '',
    style: str = '',
    sep: str = ' ',
    end: str = '\n',
    ignore: bool = False,
    flush: bool = False,
    nowrapper: bool = False
) -> None:
    """Enhanced print function"""

    texts = [str(t) for t in texts]

    # we have line endings
    if any(
        ['\n' in t for t in texts]
    ):
        for i, t in enumerate(texts):
            if t.endswith('\n'):
                texts[i + 1] = '\n' + texts[i + 1]  # update next string by adding line end
                texts[i] = t[:-1]  # remove line end from current string
        nowrapper = True

        texts = list(filter(None, texts))  # remove empty strings

    if logging:
        logging.info(sep.join(texts))

    if ignore:
        return

    colors = None
    if isinstance(color, dict):
        colors = color
        color = None

    if len(texts):
        try:
            prefix = ' ' * indent
        except TypeError:
            prefix = indent or ''

        suffix = ''
        prefix_len_subtract = 0
        if color or style:
            prefix += getattr(
                Fore,
                color.upper(), ''
            ) + getattr(
                Style, style.upper(),
                ''
            )
            prefix_len_subtract = len(prefix) - 2
            suffix = COLOR_RESET

        if colors:
            texts_colored = []
            for i, t in enumerate(texts, start=1):
                p = s = ''
                if i in colors:
                    p = getattr(Fore, colors[i].upper())
                    s = COLOR_RESET

                texts_colored.append(p + t + s)

            texts = texts_colored

        if isinstance(list_bullet, bool):
            if list_bullet:
                list_bullet = LIST_BULLET
            else:
                list_bullet = ''

        bullet_sep = ' '
        prefix += list_bullet + bullet_sep if list_bullet else ''

        try:  # when there is no terminal, i.e. cron-job
            term_rows, term_columns = map(
                int,
                os.popen('stty size', 'r').read().split()
            )
            wrapper = textwrap.TextWrapper(
                initial_indent=prefix,
                width=term_columns,
                subsequent_indent=' ' * (len(prefix) - prefix_len_subtract)
            )
        except ValueError:
            nowrapper = True

        if flush or nowrapper:
            print(
                prefix + texts[0],
                *texts[1:],
                suffix,
                sep=sep,
                end=end,
                flush=flush
            )
        else:
            msg = sep.join(
                [t for t in texts]
            ) + suffix + end

            print(wrapper.fill(msg))

    else:
        print()


##  format file size
#
#   inspired by Fred Cirera, https://stackoverflow.com/a/1094933/1690805
#   @param IEC: use binary prefixes as established by the International Electrotechnical Commission
def format_filesize(num, suffix="B", prefix_type='binary'):
    divider = 1024.0 if prefix_type == 'binary' else 1000.0

    for unit in UNIT_PREFIXES.get(prefix_type):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"

        num /= divider

    return f"{num:.1f}Yi{suffix}"
