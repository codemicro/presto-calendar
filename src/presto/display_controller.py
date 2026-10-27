import machine
import time_util
from picovector import PicoVector
import math
import time


def lerp_colour(progress, colour_a, colour_b):
    return (
        int(colour_a[0] + ((colour_b[0] - colour_a[0]) * progress)),
        int(colour_a[1] + ((colour_b[1] - colour_a[1]) * progress)),
        int(colour_a[2] + ((colour_b[2] - colour_a[2]) * progress))
    )


class DisplayController:
    FONT_COLOUR = (0x5f, 0x5f, 0x5f)
    ORB_COLOUR = (0xdf, 0x30, 0x62)
    
    def __init__(self, comms, presto, display):
        self.comms = comms
        self.presto = presto
        self.display = display
        self.time_font_draw = PicoVector(display)
        self.time_font_draw.set_font("Roboto/Roboto-Regular.af", 20)
        self.next_up_font_draw = PicoVector(display)
        self.next_up_font_draw.set_font("Roboto/Roboto-Bold.af", 24)
        
        self.width, self.height = display.get_bounds()
        self.timer = None

        self.i = 0

    def start_loop(self):
        self.timer = machine.Timer()
        self.timer.init(period=500, mode=machine.Timer.PERIODIC, callback=lambda _: self.loop())

    def word_wrap(self, text, font, width=None):
        if width is None:
            width = self.width
            
        parts = text.split(" ")
        _, _, combi_space_width, _ = font.measure_text(". .")
        _, _, dot_width, _ = font.measure_text(".")
        space_width = combi_space_width - (dot_width * 2)

        part_lengths = [None] * len(parts)
        for i, part in enumerate(parts):
            _, _, w, _ = font.measure_text(part)
            part_lengths[i] = int(w)

        groups = [""]
        group_lengths = [0]
        for i, part in enumerate(parts):
            current_len = group_lengths[-1]
            
            if current_len == 0:
                groups[-1] += part
                group_lengths[-1] = current_len + part_lengths[i]
            elif current_len + space_width + part_lengths[i] < width:
                groups[-1] += " " + part
                group_lengths[-1] = current_len + part_lengths[i] + space_width
            else:
                groups.append(part)
                group_lengths.append(part_lengths[i])

        return list(zip(groups, group_lengths))

    def draw_time(self):
        time_str = time_util.get_time_HHMM()

        self.display.set_pen(self.display.create_pen(*self.FONT_COLOUR))

        _, _, w, h = self.time_font_draw.measure_text(time_str)
        min_pos = 10
        max_pos = self.width - w - 10
        
        period = 10000
        steps_taken = self.i % (2 * period)
        progress = (self.i % period) / period
        
        if steps_taken < period:
            pos = int(min_pos + ((max_pos - min_pos) * progress))
        else:
            pos = int(max_pos - ((max_pos - min_pos) * progress))
        
        # self.time_font_draw.text(time_str, pos, int(10 + h))
        self.display.text(time_str, pos, int(10 + h), scale=2)

    def draw_meeting_text(self, meeting_title, meeting_time_str, progress):
        padding = 5
        
        meeting_parts = self.word_wrap(meeting_title, self.next_up_font_draw)
        
        _, _, _, meeting_h = self.next_up_font_draw.measure_text(meeting_parts[0][0])
        _, _, meeting_time_w, meeting_time_h = self.time_font_draw.measure_text(meeting_time_str)

        start_height = int(self.height * 0.35)
        cursor = start_height

        self.display.set_pen(self.display.create_pen(*lerp_colour(progress, self.FONT_COLOUR, (0xff, 0xff, 0xff))))

        for (part, length) in meeting_parts:
            x_pos = int((self.width - length) / 2)
            cursor += meeting_h
            # self.next_up_font_draw.text(part, x_pos, int(cursor))
            self.display.text(part, x_pos, int(cursor), scale=2)
            cursor += padding

        # self.time_font_draw.text(meeting_time_str, int((self.width - meeting_time_w) / 2), int(cursor + meeting_time_h + padding))
        self.display.text(meeting_time_str, int((self.width - meeting_time_w) / 2), int(cursor + meeting_time_h + padding), scale=2)

    def draw_orb(self, progress):
        black = (0x00, 0x00, 0x00)
        draw_colour = lerp_colour(progress, black, self.ORB_COLOUR)

        max_radius = int(math.sqrt(((self.width/2) ** 2) + ((self.height/2) ** 2)))

        self.display.set_pen(self.display.create_pen(*draw_colour))
        self.display.circle(int(self.width/2), int(self.height/2), int(max_radius * progress))
        

    def loop(self):
        self.display.set_pen(0)
        self.display.clear()

        progress = (self.i % 25) / 25
        self.i += 1

        next_meeting = self.comms.get_next_meeting()
        if next_meeting is not None:
            meeting_name, start_unix, end_unix = next_meeting

            now = time.time()
            ten_mins_before = start_unix - (10 * 60)
            progress = max(0, ((10 * 60) - (start_unix - time.time())) / (10 * 60))
            
            if ten_mins_before < now:
                self.draw_orb(progress)
            
            self.draw_time()
            
            self.draw_meeting_text(meeting_name, time_util.format_meeting_time(start_unix, end_unix), progress)
        else:
            self.draw_time()

        self.display.text("{}".format(self.i), 10, 200, scale=2)
        
        self.presto.update()