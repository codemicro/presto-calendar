from io import BufferedWriter
import sys
import platform
import umsgpack
from pathlib import Path
import enum
import messages
import time


def mock_meeting(n):
    import datetime
    start = int((datetime.datetime.now() + datetime.timedelta(minutes=n)).timestamp())
    end = start + (60 * 30)
    return (
        "Mobile Experience Stand-Up", start, end
    )


def find_connected_device() -> Path | None:
    current_system = platform.system()
    if current_system == "Linux":
        tty_file = "/dev/ttyACM0"
    elif current_system == "Darwin":
        raise NotImplementedError("implement me")
    else:
        raise ValueError(f"platform {current_system} not supported")

    tty_file = Path(tty_file)
    
    if tty_file.exists():
        return tty_file

    return None


class DeviceState(enum.Enum):
    DISCONNECTED = enum.auto()
    UNINITIALISED = enum.auto()
    CONNECTED = enum.auto()


class DeviceController:
    tty_file: Path
    state: DeviceState
    device: BufferedWriter | None
    
    def __init__(self, tty_file: Path):
        self.tty_file = tty_file
        self.state = DeviceState.DISCONNECTED
        self.device = None

    def loop(self, mock_meeting):
        if self.state == DeviceState.DISCONNECTED:
            # self.device = self.tty_file.open("wb")
            self.state = DeviceState.UNINITIALISED

        if self.state == DeviceState.UNINITIALISED:
            with self.tty_file.open("wb") as f:
                f.write(
                    messages.set_time()
                )
            self.state = DeviceState.CONNECTED

        time.sleep(1)

        if self.state == DeviceState.CONNECTED:
            with self.tty_file.open("wb") as f:
                print("sending", mock_meeting)
                f.write(
                    messages.send_meetings([mock_meeting])
                )
                    


def main() -> int:
    device = find_connected_device()
    assert device is not None
    controller = DeviceController(device)
    for i in reversed(range(30)):
        controller.loop(mock_meeting(i))
        time.sleep(2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
