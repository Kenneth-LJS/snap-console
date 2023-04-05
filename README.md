# Snap Console
Easy-to-use interactive console for Python

-----

## Installation

You can install `Snap console` with pip

```
pip install snap-console
```

## Getting Started

`Snap console` is built on top of the `curses` library to give you access to powerful console functionality without having to deal with low-level read/writes.

To begin, you can set up the console with the following code:

```py
from snapconsole import SnapConsole

console = SnapConsole()
console.start()
# Handle console commands here
console.stop()
```

`start()` initializes the empty console, and `stop()` resets the console to how it was before. You can also use Python's context manager syntax to use the console:

```py
from snapconsole import SnapConsole

with SnapConsole() as console:
    # Handle console commands here
```

## The console

The console consists of 2 segments: the display and the input box. [default: bottom row = input, but can be tweaked]

```
with SnapConsole() as console:
    console.logs 
```
