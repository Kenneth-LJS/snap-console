from snapconsole import SnapConsole

with SnapConsole() as console:
    console.logs.append('Type anything and press "Enter"')
    for user_input in console:
        # Handle each user input
        if len(user_input) == 0:
            break

        console.logs.append('ECHO: ' + user_input)