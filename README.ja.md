log4func
===

![Software Version](http://img.shields.io/badge/Version-v0.1.0-green.svg?style=flat)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

[English Page](./README.md)

## 概要
関数やメソッドのためのログヘルパー。

## ライセンス
[MIT License](./LICENSE)

## インストール
### pip
```
pip install log4func
```

### github
```
pip install git+https://github.com/bugph0bia/log4func.git
```

## 使用方法
### `@log_start_end`
対象の関数の最初と最後をログ出力するデコレータ。  
引数に渡されたログ出力関数を使用してログ出力する。  

#### 引数

- `logging_func` (Callable): ログ出力関数。str型の引数を受け取ってログ出力できる必要がある。`print` や `logging` モジュールの `debug` `info` などを指定可能。
- `with_start` (bool): 最初のログを出力するか否かを切り替える。デフォルトは `True`。
- `with_end` (bool): 最後のログを出力するか否かを切り替える。デフォルトは `True`。

#### 使用例
```py
@log_start_end(print)
def foo(a, b):
    print(f'calc {a} + {b}')
    return a + b

foo(1, 2)
```

出力  
```sh
foo start
calc 1 + 2
foo end
```

### `@log_args_return`
対象の関数の実引数と戻り値をログ出力するデコレータ。  
引数に渡されたログ出力関数を使用してログ出力する。  

#### 引数

- `logging_func` (Callable): ログ出力関数。str型の引数を受け取ってログ出力できる必要がある。`print` や `logging` モジュールの `debug` `info` などを指定可能。
- `with_args` (bool): 引数のログを出力するか否かを切り替える。デフォルトは `True`。
- `with_return` (bool): 戻り値のログを出力するか否かを切り替える。デフォルトは `True`。
- `oneline` (bool): ログを1行にまとめるか否かを切り替える。デフォルトは `False`。

#### 使用例
```py
@log_args_return(print)
def foo(a, b):
    print(f'calc {a} + {b}')
    return a + b

foo(1, b=2)
```

出力  
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

出力  
```sh
foo args: 1, b=2
calc 1 + 2
foo return: 3
```

### `@log_traceback`
対象の関数で発生した例外のトレースバックをログ出力するデコレータ。  
引数に渡されたログ出力関数を使用してログ出力する。  

トレースバックは標準で画面に出力されるが、logging モジュール等でファイルに残したい場合に便利。  

#### 引数

- `logging_func` (Callable): ログ出力関数。str型の引数を受け取ってログ出力できる必要がある。`print` や `logging` モジュールの `debug` `info` などを指定可能。

#### 注意

- `log4func.log_traceback` がラップしている部分もトレースバックに出力される。

#### 使用例
```py
@log_traceback(print)
def foo(a, b):
    return a / b

foo(1, 0)
```

出力  
```sh
Traceback (most recent call last):
File "...\log4func.py", line 184, in wrapper
    decorated_func(*args, **kwargs)
File "...\test.py", line 2, in foo
    a / b
ZeroDivisionError: division by zero
```

### `@wraps_logging_params`
デコレータ内で関数名のログ出力を行った場合に元の関数名を出力できるようにするデコレータ。  

#### 補足説明

ある関数に自作のデコレータを適用すると、元の関数名を `func.__name__` で取得したときに、デコレータの関数名になってしまうという問題がある。
これを解決するためには、自作のデコレータに `@functool.wraps` デコレータを適用すればよい。

同様に、ある関数に自作のデコレータを適用すると、元の関数内部で logging モジュールを利用して関数名 (`%(funcName)s`) を出力するとデコレータの関数名になってしまう。
これを解決するためには、自作のデコレータに `@log4func.wraps_logging_params` デコレータを適用すれば良い。

### 注意
- `@classmethod` や `@staticmethod` と同時に使用する場合は、より内側のデコレータとする必要がある。
