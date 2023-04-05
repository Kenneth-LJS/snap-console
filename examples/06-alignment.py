from snapconsole import SnapConsole, TextboxAlignPosition, LogsAlignPosition

with SnapConsole(
    # Change the alignment between `TOP` and `BOTTOM` to see how they look
    textbox_align_position=TextboxAlignPosition.TOP,
    logs_align_position=LogsAlignPosition.TOP,
) as console:
    console.logs.append('Type anything and press "Enter"')

    console.header.append('Header line 1')
    console.header.append('Header line 2')
    console.footer.append('Footer line 1')
    console.footer.append('Footer line 2')

    for user_input in console:
        if len(user_input) == 0:
            break
        console.logs.append('ECHO: ' + user_input)
