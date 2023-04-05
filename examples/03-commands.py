from snapconsole import SnapConsole

with SnapConsole() as console:

    cur_string = ''

    console.logs.append('Commands: help, print, add [STRING], set [STRING], exit')
    for user_input in console:
        # Handle each user input
        if len(user_input) == 0:
            break

        splitted = user_input.split(' ', maxsplit=1)
        command = splitted[0].lower()

        if command == 'help':
            console.logs.append('Commands: help, print, add [STRING], set [STRING]')
        elif command == 'print':
            console.logs.append(f'Value: "{cur_string}"')
        elif command in ('add', 'set'):
            if len(splitted) < 2:
                console.logs.append(f'Error: usage "{command} [STRING]"')
                continue
            if command == 'add':
                cur_string += splitted[1]
            else:
                cur_string = splitted[1]
            console.logs.append(f'Updated value: "{cur_string}"')
        elif command == 'exit':
            break