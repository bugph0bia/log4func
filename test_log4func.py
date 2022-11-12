import unittest
from test.support import captured_stdout
import sys
import logging

import log4func


class TestWrapsLoggingParams(unittest.TestCase):
    """test of @wraps_logging_params"""

    def test_use_logger(self):
        """test with using logger"""

        # create logger that uses params "filename" and "funcName"
        def create_logger():
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(logging.Formatter('%(filename)s %(funcName)s: %(message)s'))
            logger.addHandler(handler)
            return logger

        # Test Target
        def decorator(func):
            @log4func.wraps_logging_params(func)
            def wrapper(*args, **kwargs):
                logger = create_logger()
                logger.debug('test log')
                func(*args, **kwargs)
            return wrapper

        with captured_stdout() as cstdout:

            @decorator
            def foo(a, b):
                return a + b

            foo(1, b=2)

            log = (
                'test_log4func.py foo: test log\n'
            )
            self.assertEqual(cstdout.getvalue(), log)


class TestLogStartEnd(unittest.TestCase):
    """test of @log_start_end"""

    def test_function(self):
        """test with function"""

        # Test Target
        @log4func.log_start_end(print)
        def foo(a, b):
            print(f'{a}+{b}')
            return a + b

        with captured_stdout() as cstdout:
            foo(1, b=2)

            log = (
                'TestLogStartEnd.test_function.<locals>.foo start\n'
                '1+2\n'
                'TestLogStartEnd.test_function.<locals>.foo end\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

    def test_method(self):
        """test with class methods"""

        # Test Target
        class Foo:
            @log4func.log_start_end(print)
            def instance_method(self, a, b):
                print(f'{a}+{b}')
                return a + b

            @classmethod
            @log4func.log_start_end(print)
            def class_method(cls, a, b):
                print(f'{a}+{b}')
                return a + b

            @staticmethod
            @log4func.log_start_end(print)
            def static_method(a, b):
                print(f'{a}+{b}')
                return a + b

        with captured_stdout() as cstdout:
            Foo().instance_method(1, b=2)

            log = (
                'TestLogStartEnd.test_method.<locals>.Foo.instance_method start\n'
                '1+2\n'
                'TestLogStartEnd.test_method.<locals>.Foo.instance_method end\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

        with captured_stdout() as cstdout:
            Foo.class_method(2, b=3)

            log = (
                'TestLogStartEnd.test_method.<locals>.Foo.class_method start\n'
                '2+3\n'
                'TestLogStartEnd.test_method.<locals>.Foo.class_method end\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

        with captured_stdout() as cstdout:
            Foo.static_method(3, b=4)

            log = (
                'TestLogStartEnd.test_method.<locals>.Foo.static_method start\n'
                '3+4\n'
                'TestLogStartEnd.test_method.<locals>.Foo.static_method end\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

    def test_set_args(self):
        """test with set args"""

        @log4func.log_start_end(print, with_start=False)
        def foo1(a, b):
            print(f'{a}+{b}')
            return a + b

        @log4func.log_start_end(print, with_end=False)
        def foo2(a, b):
            print(f'{a}+{b}')
            return a + b

        with captured_stdout() as cstdout:
            foo1(1, b=2)
            foo2(2, b=3)

            log = (
                '1+2\n'
                'TestLogStartEnd.test_set_args.<locals>.foo1 end\n'
                'TestLogStartEnd.test_set_args.<locals>.foo2 start\n'
                '2+3\n'
            )
            self.assertEqual(cstdout.getvalue(), log)


class TestLogArgsReturn(unittest.TestCase):
    """test of @log_args_return"""

    def test_function(self):
        """test with function"""

        # Test Target
        @log4func.log_args_return(print)
        def foo(a, b):
            print(f'{a}+{b}')
            return a + b

        with captured_stdout() as cstdout:
            foo(1, b=2)

            log = (
                'TestLogArgsReturn.test_function.<locals>.foo args:\n'
                '  1\n'
                '  b=2\n'
                '1+2\n'
                'TestLogArgsReturn.test_function.<locals>.foo return:\n'
                '  3\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

    def test_method(self):
        """test with class methods"""

        # Test Target
        class Foo:
            @log4func.log_args_return(print)
            def instance_method(self, a, b):
                print(f'{a}+{b}')
                return a + b

            @classmethod
            @log4func.log_args_return(print)
            def class_method(cls, a, b):
                print(f'{a}+{b}')
                return a + b

            @staticmethod
            @log4func.log_args_return(print)
            def static_method(a, b):
                print(f'{a}+{b}')
                return a + b

        with captured_stdout() as cstdout:
            Foo().instance_method(1, b=2)

            lines = cstdout.getvalue().splitlines()

            # check "self" argument
            self.assertIn('test_log4func.TestLogArgsReturn.test_method.<locals>.Foo object', lines.pop(1))

            # check the remaining lines
            log = (
                'TestLogArgsReturn.test_method.<locals>.Foo.instance_method args:\n'
                '  1\n'
                '  b=2\n'
                '1+2\n'
                'TestLogArgsReturn.test_method.<locals>.Foo.instance_method return:\n'
                '  3'
            )
            self.assertEqual('\n'.join(lines), log)

        with captured_stdout() as cstdout:
            Foo.class_method(2, b=3)

            lines = cstdout.getvalue().splitlines()

            # check "cls" argument
            self.assertEqual("  <class 'test_log4func.TestLogArgsReturn.test_method.<locals>.Foo'>", lines.pop(1))

            # check the remaining lines
            log = (
                'TestLogArgsReturn.test_method.<locals>.Foo.class_method args:\n'
                '  2\n'
                '  b=3\n'
                '2+3\n'
                'TestLogArgsReturn.test_method.<locals>.Foo.class_method return:\n'
                '  5'
            )
            self.assertEqual('\n'.join(lines), log)

        with captured_stdout() as cstdout:
            Foo.static_method(3, b=4)

            log = (
                'TestLogArgsReturn.test_method.<locals>.Foo.static_method args:\n'
                '  3\n'
                '  b=4\n'
                '3+4\n'
                'TestLogArgsReturn.test_method.<locals>.Foo.static_method return:\n'
                '  7\n'
            )
            self.assertEqual(cstdout.getvalue(), log)

    def test_set_args(self):
        """test with set args"""

        @log4func.log_args_return(print, with_args=False)
        def foo1(a, b):
            print(f'{a}+{b}')
            return a + b

        @log4func.log_args_return(print, with_return=False)
        def foo2(a, b):
            print(f'{a}+{b}')
            return a + b

        @log4func.log_args_return(print, oneline=True)
        def foo3(a, b):
            print(f'{a}+{b}')
            return a + b

        with captured_stdout() as cstdout:
            foo1(1, b=2)
            foo2(2, b=3)
            foo3(3, b=4)

            log = (
                '1+2\n'
                'TestLogArgsReturn.test_set_args.<locals>.foo1 return:\n'
                '  3\n'
                'TestLogArgsReturn.test_set_args.<locals>.foo2 args:\n'
                '  2\n'
                '  b=3\n'
                '2+3\n'
                'TestLogArgsReturn.test_set_args.<locals>.foo3 args: 3, b=4\n'
                '3+4\n'
                'TestLogArgsReturn.test_set_args.<locals>.foo3 return: 7\n'
            )
            self.assertEqual(cstdout.getvalue(), log)


class TestLogTraceback(unittest.TestCase):
    """test of @log_traceback"""

    def test_function(self):
        """test with function"""

        # Test Target
        @log4func.log_traceback(print)
        def foo(a, b):
            raise Exception('except!')

        with captured_stdout() as cstdout:
            with self.assertRaises(Exception):
                foo(1, b=2)

            # check only first and last line of log
            # Because the middle lines cannot be completely checked
            logs = cstdout.getvalue().splitlines()
            self.assertEqual(logs[0], 'Traceback (most recent call last):')
            self.assertEqual(logs[-1], 'Exception: except!')

    def test_method(self):
        """test with class methods"""

        # Test Target
        class Foo:
            @log4func.log_traceback(print)
            def instance_method(self, a, b):
                raise Exception('except!')

            @classmethod
            @log4func.log_traceback(print)
            def class_method(cls, a, b):
                raise Exception('except!!')

            @staticmethod
            @log4func.log_traceback(print)
            def static_method(a, b):
                raise Exception('except!!!')

        with captured_stdout() as cstdout:
            with self.assertRaises(Exception):
                Foo().instance_method(1, b=2)

            logs = cstdout.getvalue().splitlines()
            self.assertEqual(logs[0], 'Traceback (most recent call last):')
            self.assertEqual(logs[-1], 'Exception: except!')

        with captured_stdout() as cstdout:
            with self.assertRaises(Exception):
                Foo.class_method(2, b=3)

            # check only first and last line of log
            # Because the middle lines cannot be completely checked
            logs = cstdout.getvalue().splitlines()
            self.assertEqual(logs[0], 'Traceback (most recent call last):')
            self.assertEqual(logs[-1], 'Exception: except!!')

        with captured_stdout() as cstdout:
            with self.assertRaises(Exception):
                Foo.static_method(3, b=4)

            # check only first and last line of log
            # Because the middle lines cannot be completely checked
            logs = cstdout.getvalue().splitlines()
            self.assertEqual(logs[0], 'Traceback (most recent call last):')
            self.assertEqual(logs[-1], 'Exception: except!!!')
