import curses
from snapconsole import SnapConsole

NO_COLOR = -1
NO_STYLE = 0

style_combinations = [
    ('Black', curses.COLOR_BLACK, NO_COLOR, NO_STYLE),
    ('Blue', curses.COLOR_BLUE, NO_COLOR, NO_STYLE),
    ('Cyan', curses.COLOR_CYAN, NO_COLOR, NO_STYLE),
    ('Green', curses.COLOR_GREEN, NO_COLOR, NO_STYLE),
    ('Magenta', curses.COLOR_MAGENTA, NO_COLOR, NO_STYLE),
    ('Red', curses.COLOR_RED, NO_COLOR, NO_STYLE),
    ('White', curses.COLOR_WHITE, NO_COLOR, NO_STYLE),
    ('Yellow', curses.COLOR_YELLOW, NO_COLOR, NO_STYLE),
    ('Green on blue', curses.COLOR_GREEN, curses.COLOR_BLUE, NO_STYLE),
    ('White on blue', curses.COLOR_WHITE, curses.COLOR_BLUE, NO_STYLE),
    ('White on blue + bold', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_BOLD),
    ('White on blue + italic', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_ITALIC),
    ('White on blue + bold + italic', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_BOLD | curses.A_ITALIC),
]

with SnapConsole() as console:
    for i, (name, fg_color, bg_color, additional_attr) in enumerate(style_combinations, start=1):
        curses.init_pair(i, fg_color, bg_color)

        attr = curses.color_pair(i) | additional_attr
        console.logs.append([attr, name])

    console.logs.append('Press "Enter" to continue')
    console.get_input()