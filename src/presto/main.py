from presto import Presto
import time_util
import display_controller


time_util.init_clock(1792439091)
presto = Presto()
dc = display_controller.DisplayController(presto, presto.display)
dc.start_loop()

# # Setup for the Presto display
# presto = Presto(ambient_light=True)
# display = presto.display
# WIDTH, HEIGHT = display.get_bounds()

# # Couple of colours for use later
# BLUE = display.create_pen(0xfd, 0xca, 0x9d)
# WHITE = display.create_pen(255, 255, 255)

# pos = 0

# max_radius = int(math.sqrt(((WIDTH/2) ** 2) + ((HEIGHT/2) ** 2)))

# steps = max_radius

# start_time = time.time()
# duration = 60 * 10

# while True:
#     progress = ((time.time() - start_time) / duration) ** 2

#     # Clear the screen and use blue as the background colour
#     display.set_pen(0)
#     display.clear()
#     # Set the pen to a different colour otherwise we won't be able to see the text!
#     display.set_pen(display.create_pen(0xfd - int(0xfd * (1 - progress)), 0xca - int(0xca * (1 - progress)), 0x9d - int(0x9d * (1-progress))))

#     display.circle(int(WIDTH/2), int(HEIGHT/2), pos)
#     # Finally we update the screen with our changes :)
#     presto.update()
#     time.sleep(0.5)
#     pos = int(progress * steps)
#     if pos > max_radius:
#         pos = 0
#         start_time = time.time()