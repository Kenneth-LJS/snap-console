import asyncio

from snapconsole import SnapConsole

async def console_counter_task(console):
    counter = 1
    while True:
        await asyncio.sleep(1)
        console.logs.append(f'Counter: {counter}')
        counter += 1

async def main():
    with SnapConsole() as console:
        counter_task = asyncio.create_task(console_counter_task(console))

        console.logs.append('Type anything and press "Enter"')

        # Loop using "async for" loop instead of "for"
        async for user_input in console:
            if len(user_input) == 0:
                break

            console.logs.append('ECHO: ' + user_input)

        counter_task.cancel()

asyncio.run(main())