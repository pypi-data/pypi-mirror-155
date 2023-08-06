"""
Module: '_thread' on micropython-v1.18-rp2
"""
# MCU: {'family': 'micropython', 'sysname': 'rp2', 'version': '1.18.0', 'build': '', 'mpy': 5637, 'port': 'rp2', 'platform': 'rp2', 'name': 'micropython', 'arch': 'armv7m', 'machine': 'Arduino Nano RP2040 Connect with RP2040', 'nodename': 'rp2', 'ver': 'v1.18', 'release': '1.18.0'}
# Stubber: 1.5.3
from typing import Any


class LockType():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def acquire(self, *args, **kwargs) -> Any:
        ...

    def locked(self, *args, **kwargs) -> Any:
        ...

    def release(self, *args, **kwargs) -> Any:
        ...

def allocate_lock(*args, **kwargs) -> Any:
    ...

def exit(*args, **kwargs) -> Any:
    ...

def get_ident(*args, **kwargs) -> Any:
    ...

def stack_size(*args, **kwargs) -> Any:
    ...

def start_new_thread(*args, **kwargs) -> Any:
    ...

