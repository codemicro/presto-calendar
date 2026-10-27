from presto import Presto
from communication_controller import CommunicationController
from display_controller import DisplayController
import time


presto = Presto()
cc = CommunicationController()
dc = DisplayController(cc, presto, presto.display)

while True:
    cc.loop()
    dc.loop()
    time.sleep(0.5)
