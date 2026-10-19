import machine
import time_util
from picovector import PicoVector


class DisplayController:
    FONT_COLOUR = (0x5f, 0x5f, 0x5f)
    
    def __init__(self, presto, display):
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

    def loop(self):
        self.display.set_pen(0)
        self.display.clear()

        time_str = time_util.get_time_HHMM()
        self.display.set_pen(self.display.create_pen(*self.FONT_COLOUR))

        self.display.text("{}".format(self.i), 10, 10, scale=2)
        self.i += 1

        _, _, w, h = self.time_font_draw.measure_text(time_str)
        self.time_font_draw.text(time_str, int(self.width - w - 10), int(10 + h))

        padding = 5
        
        meeting = "Mobile Experience Stand-Up"
        meeting_parts = self.word_wrap(meeting, self.next_up_font_draw)
        
        meeting_time = "15:00-15:15"
        
        _, _, _, meeting_h = self.next_up_font_draw.measure_text(meeting_parts[0][0])
        _, _, meeting_time_w, meeting_time_h = self.time_font_draw.measure_text(meeting_time)

        combined_height = (meeting_h * len(meeting_parts)) + (padding * (len(meeting_parts) - 1))
        start_height = int((self.height - combined_height) / 2)
        for i, (part, length) in enumerate(meeting_parts):
            self.next_up_font_draw.text(part, int((self.width - length) / 2), int(start_height + (meeting_h * i + 1) + (padding * i)))
        self.time_font_draw.text(meeting_time, int((self.width - meeting_time_w) / 2), int(start_height + (meeting_h * len(meeting_parts)) + (padding * (len(meeting_parts)))))

        self.presto.update()