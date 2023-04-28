#!/usr/bin/env python3

import logging

"""Context manager script.

Task. Create a context manager that would record all exceptions that occur in
the context and write them to a log file. Exceptions should only be caught, not
silenced. That is, if an exception occurred after exiting the context manager, 
it will appear further.
"""


class ExceptionLogger:
    def __init__(self, log_file):
        self.log_file = log_file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.basicConfig(filename=self.log_file, level=logging.DEBUG)
            # log the exception and its traceback to the file
            logging.exception('Exception occurred')
            # add empty line between exception logs
            logging.info('\n')
        return False

if __name__ == '__main__':

    # Exception: NameError
    with ExceptionLogger('exceptions.log'):
        a = 10
        # 'c' is not defined
        b = c

    # Exception: ZeroDivisionError
    with ExceptionLogger('exceptions.log'):
        a = 10
        b = 0
        # division by zero
        c = a / b

    # Exception: FileNotFoundError
    with ExceptionLogger('exceptions.log'):
        with open('nonexistent_file.txt') as f:
            # file is not exist
            contents = f.read() # file is not exist

    # Exception: TypeError
    with ExceptionLogger('exceptions.log'):
        a = 'hello'
        b = 10
        # different types division
        c = a / b

    # Exception: Everything is OK
    with ExceptionLogger('exceptions.log'):
        a = 10
        b = 5
        c = a / b
        print(f'{a} / {b} = {c}')

