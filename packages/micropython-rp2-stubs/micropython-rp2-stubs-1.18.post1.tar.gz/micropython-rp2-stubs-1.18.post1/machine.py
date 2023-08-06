"""
Module: 'machine' on micropython-v1.18-rp2
"""
# MCU: {'family': 'micropython', 'sysname': 'rp2', 'version': '1.18.0', 'build': '', 'mpy': 5637, 'port': 'rp2', 'platform': 'rp2', 'name': 'micropython', 'arch': 'armv7m', 'machine': 'Arduino Nano RP2040 Connect with RP2040', 'nodename': 'rp2', 'ver': 'v1.18', 'release': '1.18.0'}
# Stubber: 1.5.3
from typing import Any


class ADC():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    CORE_TEMP = 4 # type: int
    def read_u16(self, *args, **kwargs) -> Any:
        ...


class I2C():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def readinto(self, *args, **kwargs) -> Any:
        ...

    def start(self, *args, **kwargs) -> Any:
        ...

    def stop(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def readfrom(self, *args, **kwargs) -> Any:
        ...

    def readfrom_into(self, *args, **kwargs) -> Any:
        ...

    def readfrom_mem(self, *args, **kwargs) -> Any:
        ...

    def readfrom_mem_into(self, *args, **kwargs) -> Any:
        ...

    def scan(self, *args, **kwargs) -> Any:
        ...

    def writeto(self, *args, **kwargs) -> Any:
        ...

    def writeto_mem(self, *args, **kwargs) -> Any:
        ...

    def writevto(self, *args, **kwargs) -> Any:
        ...


class I2S():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def readinto(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    MONO = 0 # type: int
    RX = 0 # type: int
    STEREO = 1 # type: int
    TX = 1 # type: int
    def deinit(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def irq(self, *args, **kwargs) -> Any:
        ...

    def shift(self, *args, **kwargs) -> Any:
        ...


class PWM():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def deinit(self, *args, **kwargs) -> Any:
        ...

    def duty_ns(self, *args, **kwargs) -> Any:
        ...

    def duty_u16(self, *args, **kwargs) -> Any:
        ...

    def freq(self, *args, **kwargs) -> Any:
        ...

PWRON_RESET = 1 # type: int

class Pin():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def value(self, *args, **kwargs) -> Any:
        ...

    ALT = 3 # type: int
    IN = 0 # type: int
    IRQ_FALLING = 4 # type: int
    IRQ_RISING = 8 # type: int
    OPEN_DRAIN = 2 # type: int
    OUT = 1 # type: int
    PULL_DOWN = 2 # type: int
    PULL_UP = 1 # type: int
    def high(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def irq(self, *args, **kwargs) -> Any:
        ...

    def low(self, *args, **kwargs) -> Any:
        ...

    def off(self, *args, **kwargs) -> Any:
        ...

    def on(self, *args, **kwargs) -> Any:
        ...

    def toggle(self, *args, **kwargs) -> Any:
        ...


class RTC():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def datetime(self, *args, **kwargs) -> Any:
        ...


class SPI():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def read(self, *args, **kwargs) -> Any:
        ...

    def readinto(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    LSB = 0 # type: int
    MSB = 1 # type: int
    def deinit(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def write_readinto(self, *args, **kwargs) -> Any:
        ...


class Signal():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def value(self, *args, **kwargs) -> Any:
        ...

    def off(self, *args, **kwargs) -> Any:
        ...

    def on(self, *args, **kwargs) -> Any:
        ...


class SoftI2C():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def readinto(self, *args, **kwargs) -> Any:
        ...

    def start(self, *args, **kwargs) -> Any:
        ...

    def stop(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def readfrom(self, *args, **kwargs) -> Any:
        ...

    def readfrom_into(self, *args, **kwargs) -> Any:
        ...

    def readfrom_mem(self, *args, **kwargs) -> Any:
        ...

    def readfrom_mem_into(self, *args, **kwargs) -> Any:
        ...

    def scan(self, *args, **kwargs) -> Any:
        ...

    def writeto(self, *args, **kwargs) -> Any:
        ...

    def writeto_mem(self, *args, **kwargs) -> Any:
        ...

    def writevto(self, *args, **kwargs) -> Any:
        ...


class SoftSPI():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def read(self, *args, **kwargs) -> Any:
        ...

    def readinto(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    LSB = 0 # type: int
    MSB = 1 # type: int
    def deinit(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def write_readinto(self, *args, **kwargs) -> Any:
        ...


class Timer():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    ONE_SHOT = 0 # type: int
    PERIODIC = 1 # type: int
    def deinit(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...


class UART():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def any(self, *args, **kwargs) -> Any:
        ...

    def read(self, *args, **kwargs) -> Any:
        ...

    def readinto(self, *args, **kwargs) -> Any:
        ...

    def readline(self, *args, **kwargs) -> Any:
        ...

    def write(self, *args, **kwargs) -> Any:
        ...

    CTS = 1 # type: int
    INV_RX = 2 # type: int
    INV_TX = 1 # type: int
    RTS = 2 # type: int
    def sendbreak(self, *args, **kwargs) -> Any:
        ...


class WDT():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def feed(self, *args, **kwargs) -> Any:
        ...

WDT_RESET = 3 # type: int
def bitstream(*args, **kwargs) -> Any:
    ...

def bootloader(*args, **kwargs) -> Any:
    ...

def deepsleep(*args, **kwargs) -> Any:
    ...

def disable_irq(*args, **kwargs) -> Any:
    ...

def enable_irq(*args, **kwargs) -> Any:
    ...

def freq(*args, **kwargs) -> Any:
    ...

def idle(*args, **kwargs) -> Any:
    ...

def lightsleep(*args, **kwargs) -> Any:
    ...

mem16 : Any ## <class 'mem'> = <16-bit memory>
mem32 : Any ## <class 'mem'> = <32-bit memory>
mem8 : Any ## <class 'mem'> = <8-bit memory>
def reset(*args, **kwargs) -> Any:
    ...

def reset_cause(*args, **kwargs) -> Any:
    ...

def soft_reset(*args, **kwargs) -> Any:
    ...

def time_pulse_us(*args, **kwargs) -> Any:
    ...

def unique_id(*args, **kwargs) -> Any:
    ...

