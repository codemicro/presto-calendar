import machine
import time


_is_clock_init = False


def init_clock(timestamp):
    global _is_clock_init
    t=time.gmtime(timestamp)
    machine.RTC().datetime((t[0], t[1], t[2], t[6], t[3], t[4], t[5], 0))
    _is_clock_init = True


def is_clock_init():
    return _is_clock_init


def get_time_HHMM():
    if not _is_clock_init:
        return "--:--"

    _, _, _, _, hour, min, _, _ = machine.RTC().datetime()
    return "{:0>2}:{:0>2}".format(hour, min)