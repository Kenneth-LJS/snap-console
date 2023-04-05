import curses
from snapconsole import SnapConsole

style_combinations = [
    ('Normal', curses.A_NORMAL),
    ('Bold', curses.A_BOLD),
    ('Italic', curses.A_ITALIC),
    ('Underline', curses.A_UNDERLINE),
    ('Blink', curses.A_BLINK),
    ('Reverse', curses.A_REVERSE),
    ('Standout', curses.A_STANDOUT),
    ('Dim', curses.A_DIM),
    ('Invis', curses.A_INVIS),
    ('Protect', curses.A_PROTECT),
    ('Horizontal', curses.A_HORIZONTAL),
    ('Vertical', curses.A_VERTICAL),
    ('Left', curses.A_LEFT),
    ('Right', curses.A_RIGHT),
    ('Low', curses.A_LOW),
    ('Top', curses.A_TOP),
    ('Bold + Italic', curses.A_BOLD | curses.A_ITALIC),
    ('Bold + Underline', curses.A_BOLD | curses.A_UNDERLINE),
    ('Bold + Italic + Underline', curses.A_BOLD | curses.A_ITALIC | curses.A_UNDERLINE),
]

with SnapConsole() as console:
    console.logs.append('Text styles can be applied with attributes:')
    for name, attr in style_combinations:
        console.logs.append([attr, name])

    console.logs.append('Press "Enter" to continue')
    console.get_input()