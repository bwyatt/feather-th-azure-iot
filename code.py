import time
import board
import adafruit_ahtx0
import terminalio
from displayio import Group
from adafruit_display_text import bitmap_label

delay = 5 # Time between readings, in seconds

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

text_area = bitmap_label.Label(terminalio.FONT, scale=2)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height // 2)
main_group = Group()
main_group.append(text_area)
board.DISPLAY.show(main_group)

while (True):
    temp_c = sensor.temperature
    temp_f = (temp_c * 1.8) + 32
    humidity = sensor.relative_humidity
    
    text_area.text = "Temp (C): {}\nTemp(F): {}\nRH: {}%".format(temp_c, temp_f, humidity)

    time.sleep(delay)
