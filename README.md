log4func
===

![Software Version](http://img.shields.io/badge/Version-v0.1.0-green.svg?style=flat)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

[Japanese Page](./README.ja.md)

## Overview
Log helpers for functions and methods.

## License
[MIT License](./LICENSE)

## Installation
### pip
```
pip install log4func
```

### github
```
pip install git+https://github.com/bugph0bia/log4func.git
```

## Usage
### `@log_start_end`
Decorator that logs out the start and end of the target function.  
Log output using the function passed as argument.  

#### Parameter

- `logging_func` (Callable): Log output function, must be able to accept an argument of type `str` and log it. Can be `print` or `logging` module's `debug`, `info`, and more.
- `with_start` (bool): Toggles whether or not the start log is output. Default is `True`.
- `with_end` (bool): Toggles whether or not the end log is output. Default is `True`.

#### Example
```py
@log_start_end(print)
def foo(a, b):
    print(f'calc {a} + {b}')
    return a + b

foo(1, 2)
```

Output  
```sh
foo start
calc 1 + 2
foo end
```

### `@log_args_return`
Decorator that logs real arguments and return values of the target function.  
Log output using the function passed as argument.  

#### Parameter

- `logging_func` (Callable): Log output function, must be able to accept an argument of type `str` and log it. Can be `print` or `logging` module's `debug`, `info`, and more.
- `with_args` (bool): Toggles whether or not the arguments log is output. Default is `True`.
- `with_return` (bool): Toggles whether or not the return log is output. Default is `True`.
- `oneline` (bool): Toggles whether or not logs are combined into a single line. Default is `False`.

#### Example
```py
@log_args_return(print)
def foo(a, b):
    print(f'calc {a} + {b}')
    return a + b

foo(1, b=2)
```

Output  
```sh
foo args:
  1
  b=2
calc 1 + 2
foo return:
  3
```

```py
@log_args_return(print, oneline=True)
def foo(a, b):
    print(f'calc {a} + {b}')
    return a + b

foo(1, b=2)
```

Output  
```sh
foo args: 1, b=2
calc 1 + 2
foo return: 3
```

### `@log_traceback`
Decorator that logs out a traceback of exceptions raised by the target function.  
Log output using the function passed as argument.  

Traceback is output to the screen by default, but it is useful if you want to keep it in a file. (e.g. in the logging module)  

#### Parameter

- `logging_func` (Callable): Log output function, must be able to accept an argument of type `str` and log it. Can be `print` or `logging` module's `debug`, `info`, and more.

#### Note

- The part that `log4func.log_traceback` wraps is also output to traceback.

#### Example
```py
@log_traceback(print)
def foo(a, b):
    return a / b

foo(1, 0)
```

Output  
```sh
Traceback (most recent call last):
File "...\log4func.py", line 184, in wrapper
    decorated_func(*args, **kwargs)
File "...\test.py", line 2, in foo
    a / b
ZeroDivisionError: division by zero
```

### `@wraps_logging_params`
Decorator that allows the original function name to be output when the function name is logged in the decorator.  

#### Supplemental Explanation

There is a problem that if you apply your own decorator to a function, the function name of the decorator becomes the function name of the original function when you get the original function name with `func.__name__`.
To solve this problem, you can apply `@functool.wraps` decorator to your own decorator.

Similarly, if you apply your own decorator to a function, the function name (`%(funcName)s`) output inside the original function using the logging module will be the decorator's function name.
To solve this problem, you can apply `@log4func.wraps_logging_params` decorator to your own decorator.

### Note
- If used with `@classmethod` or `@staticmethod`, it must be an inner decorator.
