# ccaerrors

Universal error handling for python functions.

## Usage

```
import sys

from ccaerrors import errorNotify

def somefunction():
    try:
        pass
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)

```

### `errorNotify`

print the function name and the Exception details to stdout.

### `errorRaise`

print the function name and the Exception details to stdout and also re-raise the Exception

### `errorExit`

print the function name and the Exception details to stdout. Exit the script by calling `sys.exit()`.
