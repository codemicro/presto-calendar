import time
import umsgpack
import sys
import time_util
import select


class TermRead:
    """
    We create  a select.poll() object called spoll, and register the standard input (sys.stdin) with the POLLIN
    flag, indicating that we want to wait for the standard input to be ready for reading.

    When we call spoll.poll(0), the 0 parameter specifies a milliseconds timeout value of 0, 
    which means that the poll() method will return immediately with a list of file descriptors that
    have events to process, or an empty list if no events are ready to be processed.

    This allows us to check if there's input available on sys.stdin without waiting for any input to arrive.
    """
    def __init__(self):
        self.spoll = select.poll()
        self.spoll.register(sys.stdin, select.POLLIN)
        
    
    def read(self):
        txt = b""
        while self.spoll.poll(0):
            # see the other versions here for utf-8 characters
            txt += sys.stdin.buffer.read(1)
        return txt


class CommunicationController:
    def __init__(self):
        self.reader = TermRead()
        self.meetings = []

    def loop(self):
        buf = self.reader.read()
        if len(buf) == 0:
            return
        
        unpacked = umsgpack.unpackb(buf)
        print("unpacked", unpacked)
        message_type = unpacked["t"]
    
        if message_type == "settime":
            time_util.init_clock(unpacked["unix"])
    
        if message_type == "meetings":
            self.meetings = unpacked["meetings"]

    def get_next_meeting(self):
        now = time.time()
        print(self.meetings)
        for meeting in self.meetings:
            if meeting[1] > now or meeting[2] + 60 > now:
                return meeting
        return None
        