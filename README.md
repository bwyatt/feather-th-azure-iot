# feather-th-azure-iot
 An internet-connected temperature and humidity monitor for 3D printer enclosures based on the [Adafruit Feather TFT ESP32-S3](https://www.adafruit.com/product/5483) board and [AHT20 breakout sensor](https://www.adafruit.com/product/4566). 
 
 Code will be written in CircuitPython, and cloud functionality will run through Microsoft Azure, with an emphasis on their low- and no-cost service tiers.

I created this project both to learn more about CircuitPython as well as Azure's IOT services. (Disclosure: I work for Microsoft, but this project is in no way sponsored or endorsed by the company.)

Feature planning & roadmaps will be maintained in this repo's Issues.

# Requirements

* Firmware: [CircuitPython v8.x for ESP32-S3 TFT PSRAM](https://circuitpython.org/board/adafruit_feather_esp32s3_tft/) (currently in alpha)
* Python Libraries:
    * [Adafruit CircuitPython library bundle for v8.x](https://circuitpython.org/libraries) (currently in alpha)
    * [Adafruit_CircuitPython_AzureIoT library](https://docs.circuitpython.org/projects/azureiot/en/latest/)

# Configuration

Configure the device's behavior by modifying the variables under the `# Configuration` comment immediately following the `import` statements.

|Variable|Description|
|--------|-----------|
|delay|The amount of time to wait between sensor readings, in seconds|
|temp_warning_c|The minimum temperature, in Celcius, at which a warning status will be triggered. Values less than this number will be considered OK.|
|temp_critical_c|The minimum temperature, in Celcius, which should be considered critical|
|humid_warning|The minimum relative humidity at which a warning status will be triggered. Values less than this number will be considered OK.|
|humid_critical|The minimum relative humidity which should be considered critical|

# Status LED

The onboard NeoPixel is used as an indicator of overall status.

|Color|Indication|
|-----|----------|
|Red|One or both sensor values are in a Critical status.|
|Yellow|One or both sensor values are in a Warning status|
|Green|All sensor values are OK|
