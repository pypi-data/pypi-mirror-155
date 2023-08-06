# -*- coding: utf-8 -*-
import sys
from .print_tools import print_


## Wait for a key press on the console and return it
def wait_for_key(
    text: str = 'continue: press any button',
    color: str = 'black',
    list_bullet: (bool, str) = False
) -> 'None or str':
    ''' Wait for a key press on the console and return it.'''

    if text:
        print_(
            text,
            color=color,
            list_bullet=list_bullet
        )

    result = None

    import termios
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO

    termios.tcsetattr(
        fd,
        termios.TCSANOW,
        newattr
    )

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(
            fd,
            termios.TCSAFLUSH,
            oldterm
        )

    return result
