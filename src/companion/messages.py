import umsgpack
from datetime import datetime


def set_time() -> bytes:
    msg = {
        "t": "settime",
        "unix": int(datetime.now().timestamp()) 
    }
    return umsgpack.packb(msg)


def send_meetings(meetings) -> bytes:
    msg = {
        "t": "meetings",
        "meetings": meetings
    }
    return umsgpack.packb(msg)
