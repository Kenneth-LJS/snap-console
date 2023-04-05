import curses
from snapconsole import SnapConsole

style_combinations = [
    ('Black', curses.COLOR_BLACK, -1, 0),
    ('Blue', curses.COLOR_BLUE, -1, 0),
    ('Cyan', curses.COLOR_CYAN, -1, 0),
    ('Green', curses.COLOR_GREEN, -1, 0),
    ('Magenta', curses.COLOR_MAGENTA, -1, 0),
    ('Red', curses.COLOR_RED, -1, 0),
    ('White', curses.COLOR_WHITE, -1, 0),
    ('Yellow', curses.COLOR_YELLOW, -1, 0),
    ('Green on blue', curses.COLOR_GREEN, curses.COLOR_BLUE, 0),
    ('White on blue', curses.COLOR_WHITE, curses.COLOR_BLUE, 0),
    ('White on blue + bold', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_BOLD),
    ('White on blue + italic', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_ITALIC),
    ('White on blue + bold + italic', curses.COLOR_WHITE, curses.COLOR_BLUE, curses.A_BOLD + curses.A_ITALIC),
]

with SnapConsole() as console:
    for i, (name, fg_color, bg_color, additional_attr) in enumerate(style_combinations, start=1):
        curses.init_pair(i, fg_color, bg_color)

        attr = curses.color_pair(i) + additional_attr
        console.logs.append([attr, name])

    console.logs.append('Press "Enter" to continue')
    console.get_input()