import time
import board
import adafruit_ahtx0
import terminalio
import neopixel
from displayio import Group
from adafruit_display_text import bitmap_label

# Configuration
delay = 1
temp_warning_c = 35
temp_critical_c = 50
humid_warning = 45
humid_critical = 55

# Board Setup
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3
temp_status = "OK" # Can be "OK", "WARN", or "CRIT"
humid_status = "OK" 

# Display Setup
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
    
    if temp_c > temp_critical_c:
        temp_status = "CRIT"
    elif temp_c > temp_warning_c:
        temp_status = "WARN"
    else:
        temp_status = "OK"

    if humidity > humid_critical:
        humid_status = "CRIT"
    elif humidity > humid_warning:
        humid_status = "WARN"
    else:
        humid_status = "OK"

    if temp_status == "CRIT" or humid_status == "CRIT":
        pixel.fill((255, 0, 0))
    elif temp_status == "WARN" or humid_status == "WARN":
        pixel.fill((255, 255, 0))
    else:
        pixel.fill((0, 255, 0))

    text_area.text = "Temp (C): {}\nTemp(F): {}\nRH: {}%".format(temp_c, temp_f, humidity)

    time.sleep(delay)
