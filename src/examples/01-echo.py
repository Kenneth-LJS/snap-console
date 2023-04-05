from snapconsole import SnapConsole

with SnapConsole() as console:
    console.logs.append('Type anything and press "Enter"')
    user_input = console.get_input()
    console.logs.append('ECHO: ' + user_input)

    console.logs.append('Press "Enter" to continue')
    # Wait for user to press "Enter"
    console.get_input()