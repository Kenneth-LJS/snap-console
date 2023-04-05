import curses
from snapconsole import SnapConsole

with SnapConsole() as console:
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    
    # Use an array of attributes+string to apply styles
    console.logs.append([
        'Styles can be changed mid-log by adding ',
        curses.color_pair(1),
        'attributes',
        curses.A_NORMAL,
        ' into the middle of the text. Feel free to add ',
        curses.color_pair(2),
        'loads',
        curses.A_NORMAL,
        ' ',
        curses.color_pair(3),
        'of',
        curses.A_NORMAL,
        ' ',
        curses.color_pair(4),
        'colors',
        curses.A_NORMAL,
        ', or even ',
        (curses.color_pair(4) | curses.A_BOLD | curses.A_BLINK),
        'combine them',
    ])

    console.logs.append('Press "Enter" to continue')
    console.get_input()