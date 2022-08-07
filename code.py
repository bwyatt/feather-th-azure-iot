import time
import socketpool
import board
import adafruit_ahtx0
import terminalio
import neopixel
import wifi
import rtc
from displayio import Group
import adafruit_ntp
from adafruit_esp32spi import adafruit_esp32spi_socket
from adafruit_display_text import bitmap_label
from adafruit_azureiot import IoTCentralDevice


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
online_mode = False

# Display Setup
main_group = Group()
ok_color = 0x00FF00
warn_color = 0xFFFF00
crit_color = 0xFF0000

temp_c_label = bitmap_label.Label(
    font=terminalio.FONT,
    text="Temp (C):",
    scale=2,
    color=ok_color,
)
temp_c_label.anchor_point = (0, 0)
temp_c_label.anchored_position = (10, 10)
main_group.append(temp_c_label)

temp_f_label = bitmap_label.Label(
    font=terminalio.FONT,
    text="Temp (F):",
    scale=2,
    color=ok_color,
)
temp_f_label.anchor_point = (0, 0)
temp_f_label.anchored_position = (10, 50)
main_group.append(temp_f_label)

humid_label = bitmap_label.Label(
    font=terminalio.FONT,
    text="RH:",
    scale=2,
    color=ok_color,
)
humid_label.anchor_point = (0, 0)
humid_label.anchored_position = (10, 90)
main_group.append(humid_label)

# Wifi Setup
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

if "ssid" in secrets:
    try:
        print("Connecting to {}".format(secrets["ssid"]))
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("Connected to {}! IP: {}".format(secrets["ssid"], wifi.radio.ipv4_address))
        online_mode = True
        #TODO: Display Wifi connected icon
    except:
        print("Wifi connection failed!")
        raise
else:
    print("SSID was not provided. Wifi will not be connected.")
    #TODO: Display Wifi off icon

if online_mode:
    try:
        print("Connecting to Azure")
        pool = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(pool, tz_offset=0)
        rtc.RTC().datetime = ntp.datetime
        print("Current time is {}".format(ntp.datetime))
        socket = pool.socket()
        device = IoTCentralDevice(socket, wifi, secrets["id_scope"], secrets["device_id"], secrets["device_sas_key"])
        device.connect()
    except:
        print("Azure connection failed!")
        raise

board.DISPLAY.show(main_group)

while (True):
    temp_c = round(sensor.temperature, 2)
    temp_f = round((temp_c * 1.8) + 32, 2)
    humidity = round(sensor.relative_humidity, 2)
    
    if temp_c > temp_critical_c:
        temp_status = "CRIT"
        temp_c_label.color = crit_color
        temp_f_label.color = crit_color
    elif temp_c > temp_warning_c:
        temp_status = "WARN"
        temp_c_label.color = warn_color
        temp_f_label.color = warn_color
    else:
        temp_status = "OK"
        temp_c_label.color = ok_color
        temp_f_label.color = ok_color

    if humidity > humid_critical:
        humid_status = "CRIT"
        humid_label.color = crit_color
    elif humidity > humid_warning:
        humid_status = "WARN"
        humid_label.color = warn_color
    else:
        humid_status = "OK"
        humid_label.color = ok_color

    if temp_status == "CRIT" or humid_status == "CRIT":
        pixel.fill((255, 0, 0))
    elif temp_status == "WARN" or humid_status == "WARN":
        pixel.fill((255, 255, 0))
    else:
        pixel.fill((0, 255, 0))

    temp_c_label.text = "Temp (C): {}".format(temp_c)
    temp_f_label.text = "Temp (F): {}".format(temp_f)
    humid_label.text = "RH: {}%".format(humidity)

    if online_mode:
        try:
            device.loop()
            telemetry_message = {"temp_c": temp_c, "temp_f": temp_f, "humidity": humidity}
            print("Sending telemetry: {}".format(telemetry_message))
            device.send_telemetry(telemetry_message)
        except:
            # TODO: Something
            raise

    time.sleep(delay)
