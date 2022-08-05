import time
import board
import adafruit_ahtx0

delay = 5 # Time between readings, in seconds

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

while (True):
    temp_c = sensor.temperature
    temp_f = (temp_c * 1.8) + 32
    humidity = sensor.relative_humidity
    
    print("Temp (C): {}, Temp(F): {}, Relative Humidity: {}%".format(temp_c, temp_f, humidity))
    time.sleep(delay)
