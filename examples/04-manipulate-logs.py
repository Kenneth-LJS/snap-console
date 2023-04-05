from snapconsole import SnapConsole

with SnapConsole() as console:
    # Logs can be manipulated like lists
    
    # Direct assignment
    console.logs = ['Log 1', 'Log 2', 'Log 3']
    console.get_input()

    # In-place operations
    console.logs += ['Log 4', 'Log 5']
    console.logs *= 3
    console.get_input()

    # Indexing
    console.logs = console.logs[-5:]
    console.get_input()

    # Other list manipulations
    console.logs.pop()
    console.logs.pop()
    console.get_input()

    console.logs.append('Press "Enter" to continue')
    console.get_input()