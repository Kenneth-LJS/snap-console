from snapconsole import SnapConsole

with SnapConsole() as console:
    console.logs.append('Type anything and press "Enter"')

    # Just like the logs, headers and footers are accessed like lists too
    console.header.append('Header line 1')
    console.header.append('Header line 2')
    console.footer.append('Footer line 1')
    console.footer.append('Footer line 2')

    for user_input in console:
        if len(user_input) == 0:
            break
        console.logs.append('ECHO: ' + user_input)