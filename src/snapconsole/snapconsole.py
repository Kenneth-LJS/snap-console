import curses
import asyncio
from contextlib import suppress
from typing import Callable, NamedTuple, Optional, Union
from dataclasses import dataclass

from snapconsole.textbox import Textbox
from snapconsole.wrappedlist import WrappedListDescriptor

LogSubEntry = Union[int, str]
LogEntry = Union[str, list[LogSubEntry]]
LogEntrySplitter = Callable[[LogEntry, int], list[LogEntry]]

def split_and_keep(input_str: str, sep=None, maxsplit=-1):
    # Split with a separator, but still keep the separator
    splitted = input_str.split(sep=sep, maxsplit=maxsplit)
    sep_str = sep if sep is not None else ''
    return [
        sep_str if i % 2 == 1 else splitted[int(i / 2)]
        for i in range(len(splitted) * 2 - 1)
    ]

def split_list(input_list: list, sep=None):
    result = []
    cur_index = 0
    while cur_index < len(input_list):
        try:
            next_index = input_list.index(sep, cur_index)
        except ValueError:
            # No more sep in list
            break
        result.append(input_list[cur_index:next_index])
        cur_index = next_index + 1
    result.append(input_list[cur_index:])
    return result

def default_log_splitter(log_entry: LogEntry, col: int):
    if isinstance(log_entry, str):
        log_entry = [log_entry]
    
    # Split new lines in text
    temp = []
    for log_sub_entry in log_entry:
        if isinstance(log_sub_entry, int):
            temp.append(log_sub_entry)
            continue
        temp += split_and_keep(log_sub_entry, '\n')
    log_entry = temp

    # Filter non-printable characters
    temp = []
    for log_sub_entry in log_entry:
        if isinstance(log_sub_entry, int) or log_sub_entry == '\n':
            temp.append(log_sub_entry)
            continue
        temp.append(''.join(filter(curses.ascii.isprint, log_sub_entry)))
    log_entry = temp

    # Split lines by line length
    temp = []
    cur_line_len = 0
    for log_sub_entry in log_entry:
        if isinstance(log_sub_entry, int) or log_sub_entry in ('', '\n'):
            temp.append(log_sub_entry)
            continue
        while len(log_sub_entry) > 0:
            sliced_len = col - cur_line_len
            cur_slice = log_sub_entry[:sliced_len]
            cur_line_len += len(cur_slice)
            temp.append(cur_slice)

            log_sub_entry = log_sub_entry[sliced_len:]
            if cur_line_len == col:
                if len(log_sub_entry) > 0:
                    temp.append('\n')
                cur_line_len = 0
    log_entry = temp

    result = split_list(log_entry, '\n')

    # Filter empty entries
    temp = []
    for line in result:
        temp.append(list(filter(lambda l: isinstance(l, int) or len(l) > 0, line)))
    result = temp

    return result

def process_line(log_entry: LogEntry, col: int, log_splitter: LogEntrySplitter):
    lines = log_splitter(log_entry, col)
    new_lines = []
    last_attr = curses.A_NORMAL
    for line in lines:
        if isinstance(line, str):
            line = [line]
        new_lines.append([last_attr] + line)
        for segment in line:
            if isinstance(segment, int):
                last_attr = segment
    return new_lines

@dataclass
class WindowCoords:
    y: int
    x: int
    height: int
    width: int

    def __post_init__(self):
        # pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol;
        # the p arguments refer to the upper left corner of the pad region to be displayed and the s arguments define a clipping box on the screen within which the pad region is to be displayed
        self.noutrefresh_coords = (
            0, 0,
            self.y, self.x,
            self.y + self.height - 1, self.x + self.width - 1
        )

def fill_pad(pad):
    print('pad size', pad.getmaxyx())
    for y in range(pad.getmaxyx()[0]):
        for x in range(pad.getmaxyx()[1]):
            with suppress(curses.error):
                pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

ConsoleSize = NamedTuple('ConsoleSize', width=int, height=int)
HANDLE_CH_NO_CH = object()
HANDLE_CH_CONTINUE = object()

class SnapConsole:
    logs = WrappedListDescriptor('_noutrefresh_display')
    header = WrappedListDescriptor('_noutrefresh_display')
    footer = WrappedListDescriptor('_noutrefresh_display')
    command_history = WrappedListDescriptor('_handle_command_history_changed')

    def __init__(
        self,
        command_store_count: int = 100,
        log_splitter: LogEntrySplitter = default_log_splitter,
        logs_align_top: bool = False,
        textbox_align_top: bool = False,
        resize_callback: Optional[Callable[[ConsoleSize], None]] = None,
    ):
        self.command_store_count = command_store_count
        self.log_splitter = log_splitter
        self.resize_callback = resize_callback
        self._logs_align_top = logs_align_top
        self._textbox_align_top = textbox_align_top

        self.logs = []
        self.header = []
        self.footer = []

        self._current_command = ''
        self._current_command_index = 0
        self._command_history = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        self._enter_curses()

        self.displaypad = curses.newpad(1, 1)
        self.arrowpad = curses.newpad(1, 1)
        self.textpadpad = curses.newpad(1, 1)
        self.textpad = Textbox(self.textpadpad, insert_mode=True)
        self.textpad.stripspaces = True

        self._init_size()
        self.do_draw()

    def stop(self):
        self._exit_curses()
    
    def _enter_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(1)
        
        curses.start_color()
        curses.use_default_colors()

    def _exit_curses(self):
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _get_coords(self, window_type):
        scr_height, scr_width = self.stdscr.getmaxyx()
        if window_type == 'display':
            return WindowCoords(
                y=1 if self.textbox_align_top else 0,
                x=0,
                height=scr_height - 1,
                width=scr_width,
            )
        elif window_type == 'arrow':
            return WindowCoords(
                y=0 if self.textbox_align_top else scr_height - 1,
                x=0,
                height=1,
                width=2,
            )
        elif window_type == 'text':
            return WindowCoords(
                y=0 if self.textbox_align_top else scr_height - 1,
                x=2,
                height=1,
                width=scr_width - 2,
            )

    def _init_size(self):
        with suppress(curses.error):
            window_coords = self._get_coords('display')
            self.displaypad.resize(window_coords.height, window_coords.width)
            window_coords = self._get_coords('arrow')
            self.arrowpad.resize(window_coords.height, window_coords.width)
            window_coords = self._get_coords('text')
            self.textpadpad.resize(window_coords.height, window_coords.width)

    def handle_resize(self):
        self._init_size()
        self.do_draw()
        if self.resize_callback is not None:
            height, width = self.stdscr.getmaxyx()
            self.resize_callback(ConsoleSize(width=width, height=height))
        
    def do_draw(self):
        self.refresh_display()
        self.refresh_arrow()
        self.refresh_textpad()

    def refresh_display(self):
        self.displaypad.erase()

        height, width = self.displaypad.getmaxyx()

        height_left = height
        footer_lines = []
        for entry in reversed(self.footer):
            footer_lines += reversed(process_line(entry, width, self.log_splitter))
            if len(footer_lines) >= height_left:
                break
        footer_lines = footer_lines[:height_left]
        footer_lines.reverse()
        height_left -= len(footer_lines)

        header_lines = []
        for entry in self.header:
            header_lines += process_line(entry, width, self.log_splitter)
            if len(header_lines) >= height_left:
                break
        header_lines = header_lines[:height_left]
        height_left -= len(header_lines)

        log_lines = []
        for entry in reversed(self.logs):
            log_lines += reversed(process_line(entry, width, self.log_splitter))
            if len(log_lines) >= height_left:
                break
        log_lines = log_lines[:height_left]
        log_lines.reverse()
        height_left -= len(log_lines)

        if self.logs_align_top:
            lines = header_lines + log_lines + ([[]] * height_left) + footer_lines
        else:
            lines = header_lines + ([[]] * height_left) + log_lines + footer_lines

        for y, line in enumerate(lines):
            cur_attr = curses.A_NORMAL
            cur_x = 0
            if isinstance(line, str):
                line = [line]
            for segment in line:
                if isinstance(segment, int):
                    cur_attr = segment
                else:
                    with suppress(curses.error):
                        self.displaypad.insnstr(y, cur_x, segment, width - cur_x, cur_attr)
                    cur_x += len(segment)

        self.displaypad.overwrite(self.stdscr, *self._get_coords('display').noutrefresh_coords)

    def refresh_arrow(self):
        with suppress(curses.error):
            self.arrowpad.addstr(0, 0, '> ')

        self.arrowpad.overwrite(self.stdscr, *self._get_coords('arrow').noutrefresh_coords)

    def refresh_textpad(self):
        y, x = self.textpadpad.getyx()
        coords = self._get_coords('text')

        self.textpadpad.overwrite(self.stdscr, *coords.noutrefresh_coords)
        self.stdscr.move(y + coords.y, x + coords.x)

    def _noutrefresh_display(self):
        # Private wrapped for `noutrefresh_display`, silently returns if console has not been initialized
        # Calling the public one is preferred so it fails noisily
        try:
            self.stdscr
        except AttributeError:
            return
        self.refresh_display()

    def _add_command_history(self, cmd):
        if len(self._command_history) > 0 and self._command_history[-1] == cmd:
            return
        self._command_history.append(cmd)
        if len(self._command_history) > self.command_store_count:
            self._command_history = self._command_history[-self.command_store_count:]

    def _handle_input_ch(self, input_ch):
        if input_ch == -1:
            return HANDLE_CH_NO_CH
        elif input_ch == curses.KEY_RESIZE:
            self.handle_resize()
            return HANDLE_CH_CONTINUE
        elif input_ch in (curses.KEY_UP, curses.KEY_DOWN):
            if input_ch == curses.KEY_DOWN and self.current_command_index > 0:
                self.current_command_index -= 1
            elif input_ch == curses.KEY_UP and self.current_command_index < len(self.command_history):
                self.current_command_index += 1
            return HANDLE_CH_CONTINUE
        elif input_ch in (ord('\r'), ord('\n'), curses.PADENTER):
            cmd = self.textpad.gather()
            self._add_command_history(cmd)
            self._current_command_index = 0
            self.textpadpad.erase()
            self.textpadpad.move(0, 0)
            self.refresh_textpad()
            return cmd
        else:
            self.stdscr.touchwin()
            self.textpad.do_command(input_ch)
            if curses.ascii.isprint(input_ch):
                cursor_pos = self.textpadpad.getyx()
                self._current_command = self.textpad.gather()
                self._current_command_index = 0
                self.textpadpad.move(*cursor_pos)
            self.refresh_textpad()
            return HANDLE_CH_CONTINUE

    def get_input(self):
        self.stdscr.nodelay(True) # blocking read
        self.stdscr.timeout(-1) # blocking read
        while True:
            input_ch = self.stdscr.getch()
            result = self._handle_input_ch(input_ch)
            if result is HANDLE_CH_CONTINUE:
                continue
            else:
                return result

    async def async_get_input(self):
        self.stdscr.nodelay(True) # non-blocking read
        self.stdscr.timeout(0) # non-blocking read
        while True:
            input_ch = self.stdscr.getch()
            result = self._handle_input_ch(input_ch)
            if result is HANDLE_CH_CONTINUE:
                continue
            elif result is HANDLE_CH_NO_CH:
                await asyncio.sleep(0.01)
            else:
                return result

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_input()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.async_get_input()

    @property
    def logs_align_top(self):
        return self._logs_align_top

    @logs_align_top.setter
    def logs_align_top(self, new_val: bool):
        self._logs_align_top = new_val
        self.do_draw()

    @property
    def textbox_align_top(self):
        return self._textbox_align_top

    @textbox_align_top.setter
    def textbox_align_top(self, new_val: bool):
        self._textbox_align_top = new_val
        self._init_size()
        self.do_draw()

    @property
    def current_command(self):
        if self._current_command_index == 0:
            return self._current_command
        else:
            return self.command_history[-self._current_command_index]

    @current_command.setter
    def current_command(self, command):
        self._current_command = command
        self._current_command_index = 0
        self._update_cur_command()
   
    @property
    def current_command_index(self):
        return self._current_command_index

    @current_command_index.setter
    def current_command_index(self, command_index):
        if command_index < 0 or command_index > len(self.command_history):
            raise ValueError('Value should be between 0 to len(self.command_history) inclusive')
        self._current_command_index = command_index
        self._update_cur_command()

    def _handle_command_history_changed(self):
        if len(self._command_history) > self.command_store_count:
            self._command_history = self._command_history[-self.command_store_count:]
        self._current_command_index = 0
        self._update_cur_command()

    def _update_cur_command(self):
        try:
            self.stdscr
        except AttributeError:
            return
        cur_command = self.current_command
        max_width = self.textpadpad.getmaxyx()[1]
        self.textpadpad.erase()
        self.textpadpad.insnstr(0, 0, cur_command, max_width)
        self.textpadpad.move(0, min(len(cur_command), max_width - 1))
        self.refresh_textpad()