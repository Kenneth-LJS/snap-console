# Publishing

1. Run the following commands to build:

```
py -m pip install --upgrade build
py -m build
```

2. Run the following commands to publish to TestPyPI (for the first time):

```
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
```

3. Run the following commands to install the package in your library.

```
py -m venv env
.\env\Scripts\activate
```

In your new environment window:

```
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps snap-console
py -m pip install windows-curses
```

4. In your new environment window, you can test the package by opening the Python interactive console:

```
py
```

In your Python interactive console:

```python
from snapconsole import SnapConsole

with SnapConsole() as console:
    console.logs.append('Type anything and press "Enter"')
    user_input = console.get_input()
    console.logs.append('ECHO: ' + user_input)
    console.logs.append('Press "Enter" to continue')
    console.get_input()
```

5. If the package needs fixing, perform the following:

    1. Rebuild the package: `py -m build`
    2. Re-publish the package: `py -m twine upload --repository testpypi dist/*`
    3. Enter the environment window: `.\env\Scripts\activate`
    4. Update the package: `py -m pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade snap-console`

Note that if you are trying to re-publish files in the `dist` folder that have already been deployed (e.g. older build versions), you can either delete them before re-publishing, or re-publish with the command `py -m twine upload --skip-existing --repository testpypi dist/*`

After that, you can return to testing.

1. If the package looks good, you can deploy this to PyPI. In your terminal, run:

```
twine upload dist/*
```

And we are done!